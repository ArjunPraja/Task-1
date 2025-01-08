from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Get the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist. Please register first.")
            return redirect("/accounts/register/")
        
        # Authenticate the user
        user = authenticate(username=user.username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect('/accounts/login/')
        
        if not user.is_active:
            messages.error(request, "This account is inactive.")
            return redirect('/accounts/login/')
        
        login(request, user)
        return redirect('/')  # Redirect to admin or another desired page
    
    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        vpassword = request.POST.get('vpassword')
        
        if password != vpassword:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Email is already registered'})
        
        # Create a new user
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('/accounts/login/')
    
    return render(request, 'accounts/register.html')



def logout_page(request):
    logout(request)
    return redirect('/')