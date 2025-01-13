from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import ClothingItem,Cart
from django.contrib import messages
import razorpay




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




def clothing_list(request, category=None):
    """
    Displays clothing items filtered by gender category if provided,
    otherwise shows all items.
    """
    items = ClothingItem.objects.filter(gender=category) if category else ClothingItem.objects.all()
    if category!=None:
        return render(request, 'app/clothing_list.html', {'items': items,'jauners':"Shopping"})
    else:
        return render(request, 'app/clothing_list.html', {'items': items,'jauners':"Clothing"})
    


def clothing_list1(request, jauners=None):
    """
    Displays clothing items filtered by jauners if provided,
    otherwise shows all items.
    """
    items = ClothingItem.objects.filter(jauners=jauners) if jauners else ClothingItem.objects.all()
    if jauners!=None:
        return render(request, 'app/clothing_list.html', {'items': items,'jauners':"Shopping"})
    else:
        return render(request, 'app/clothing_list.html', {'items': items,'jauners':"Shopping"})
  



@login_required(login_url="/accounts/login/")
def add_to_cart(request, product_id):
    try:
        # Get the user's cart items and filter out paid ones
        cart_items = Cart.objects.filter(user=request.user)
        cart_items = [item for item in cart_items if not item.is_paid]
        
        # Calculate total price of current items in the cart
        total_price = sum(item.total_price() for item in cart_items)
        
        # Get the product to be added
        product = ClothingItem.objects.get(id=product_id)
    except ClothingItem.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('home')

    # Calculate the total price including the new item
    new_total_price = total_price + product.price

    # Check if adding the new item exceeds the limit of 100,000
    if new_total_price > 100000:
        messages.error(request, "You cannot add this item as the total price exceeds the limit of 100,000.")
        return redirect('clothing_list')
    else:
        # Check if the product already exists in the cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, clothing_item=product)
        
        if created:
            # If the item is added for the first time, show success message
            messages.success(request, f'{product.name} has been added to your cart!')
        else:
            # If the item already exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Quantity of {product.name} has been updated in your cart.')

    return redirect('view_cart')  # Redirect to the user's cart page after handling the item addition


from django.conf import settings



def update_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')
        if not quantity.isdigit() or int(quantity) <= 0:
            messages.error(request, "Invalid quantity.")
            return redirect('view_cart')

        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.quantity = int(quantity)
        cart_item.save()
        messages.success(request, f'Updated quantity for "{cart_item.clothing_item.name}".')
    return redirect('view_cart')

def delete_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        messages.success(request, f'Removed "{cart_item.clothing_item.name}" from your cart.')
    return redirect('view_cart')



from django.conf import settings
@login_required
def view_cart(request):
    # Get the user's cart items
    cart_items = Cart.objects.filter( user=request.user)
    cart_items = [item for item in cart_items if not item.is_paid]
    # Calculate total price
    total_price = sum(item.total_price() for item in cart_items) + 1

    print(total_price)

    # Ensure the total price is greater than the minimum allowed by Razorpay (usually ₹1)
    if total_price < 0:
        return HttpResponse("The total amount is too low for payment. Please add more items to your cart.", status=400)
    # Ensure the total price is greater than the minimum allowed by Razorpay (usually ₹1)
    if total_price >1000000:
        return HttpResponse("The total amount is too low for payment. Please add more items to your cart.", status=400)

    if request.method == 'POST':
        # Handle updating cart item quantity
        if 'checkout' in request.POST:
            # Implement checkout logic here (e.g., redirect to payment page)
            messages.success(request, 'Proceeding to checkout.')
            return redirect('checkout')  # Ensure you have a 'checkout' view

        # Redirect to the same cart page after POST
        return redirect('view_cart')

    # Create Razorpay client
    client = razorpay.Client(auth=(settings.KEY, settings.SECREAT))
    
    # Create the payment order
    payment = client.order.create({
        'amount': total_price * 100,  # Amount in paise
        'currency': 'INR',
        'payment_capture': 1
    })


    print("**************************")
    print(payment)
    print("**************************")

    return render(request, 'app/view_cart.html', {'cart_items': cart_items, 'total_price': total_price*100, 'payment': payment})

@login_required
def Success(request):
    """
    Handles the logic after a successful payment.
    Marks items in the cart as paid and associates the Razorpay order ID.
    """
    # Retrieve unpaid cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user, is_paid=False)
    
    # Get the Razorpay order ID from the request (ensure it's passed correctly)
    payment_id = request.GET.get('razorpay_payment_id')  # Modify based on how Razorpay sends the ID

    if not payment_id:
        return HttpResponse("Payment ID is missing. Payment verification failed.", status=400)
    
    # Mark the cart items as paid and save the Razorpay order ID
    for item in cart_items:
        item.rasor_pay_model_id = payment_id
        item.is_paid = True
        
        item.save()
    
    # Redirect the user back to the cart or a confirmation page
    return redirect('view_cart')



@login_required
def paid_cart_items(request):
    """
    View to display all paid items for the logged-in user.
    """
    # Filter for paid items
    paid_items = Cart.objects.filter(user=request.user, is_paid=True)

    # Calculate total amount of paid items (if needed)
    total_paid_price = sum(item.total_price() for item in paid_items)

    # Context data for the template
    context = {
        'paid_items': paid_items,
        'total_paid_price': total_paid_price,
    }

    # Render the paid cart items template
    return render(request, 'app/paid.html', context)


