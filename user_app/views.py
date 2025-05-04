from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User
from AnonMsg.key_manager import aes_encrypt

def index(request):
    if request.user.is_authenticated:
        return redirect('inbox')  # Redirect to inbox if user is logged in
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').capitalize()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            return render(request, 'register.html', {
                'error': 'All fields are required'
            })
        
        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })
        

        for user in User.objects.all():
            if user.get_email() == email:
                return render(request, 'register.html', {
                    'error': 'Email already exists'
                })
        

        user = User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('inbox')
        return render(request, 'register.html', {
            'error': 'Registration failed'
        })

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username').capitalize()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('inbox')
        return render(request, 'login.html', {
            'error': 'Invalid credentials'
        })

    return render(request, 'login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')