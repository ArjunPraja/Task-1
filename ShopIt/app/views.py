from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import ClothingItem,Cart
from django.contrib import messages

@login_required(login_url="/accounts/login/")
def home(request):
    return render(request, 'app/home.html')

@login_required(login_url="/accounts/login/")
def add_clothing(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        gender = request.POST.get('gender')
        price = request.POST.get('price')  # Get price from form
        photo = request.FILES.get('photo')

        # Create a new ClothingItem instance
        ClothingItem.objects.create(
            name=name,
            description=desc,
            gender=gender,
            photo=photo,
            price=price  # Include price here
        )
        return redirect('/add/')

    return render(request, 'app/add_clothing.html')




def clothing_list(request,category=None):
    if category:
        items = ClothingItem.objects.filter(gender=category)
    else:
        items = ClothingItem.objects.all()
    return render(request, 'app/clothing_list.html', {'items': items})







@login_required
def add_to_cart(request, product_id):
    try:
        # Get the clothing item to add to the cart
        product = ClothingItem.objects.get(id=product_id)
    except ClothingItem.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('home')  # Redirect to a safe page, e.g., home or product listing page

    # Check if the product already exists in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, clothing_item=product)
    
    if created:
        # If the item was added for the first time, show success message
        messages.success(request, f'{product.name} has been added to your cart!')
    else:
        # If the item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Quantity of {product.name} has been updated in your cart.')
    
    return redirect('view_cart')  # Redirect to the user's cart page after adding the item





@login_required(login_url="/accounts/login/")
def view_cart(request):
    # Get the user's cart items
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate total price
    total_price = sum(item.total_price() for item in cart_items)
    
    if request.method == 'POST':
        # Handle updating cart item quantity
        if 'update_quantity' in request.POST:
            cart_item_id = request.POST['cart_item_id']
            new_quantity = int(request.POST['quantity'])
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, 'Quantity updated successfully!')
            else:
                messages.error(request, 'Quantity must be greater than 0.')
        
        # Handle deleting an item from the cart
        elif 'delete_item' in request.POST:
            cart_item_id = request.POST['cart_item_id']
            Cart.objects.get(id=cart_item_id, user=request.user).delete()
            messages.success(request, 'Item removed from your cart.')
        
        # Handle checkout process
        elif 'checkout' in request.POST:
            # Implement checkout logic here (e.g., redirect to payment page)
            messages.success(request, 'Proceeding to checkout.')
            return redirect('checkout')  # Ensure you have a 'checkout' view
        
        # Redirect to the same cart page after POST
        return redirect('view_cart')

    return render(request, 'app/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

