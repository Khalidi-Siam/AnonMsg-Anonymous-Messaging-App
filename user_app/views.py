from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User
import base64

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
            return redirect('login')
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



@login_required
def profile(request):
    try:
        email = request.user.get_email()
    except ValueError as e:
        email = "Unable to decrypt email"
    # Profile picture logic
    try:
        profile_picture_bytes = request.user.get_profile_picture()
        print(f"Profile picture: {profile_picture_bytes is not None}, Type: {type(profile_picture_bytes) if profile_picture_bytes else None}")
        if profile_picture_bytes:
            import base64
            profile_picture_data = "data:image/png;base64," + base64.b64encode(profile_picture_bytes).decode('utf-8')
            print(f"Base64 image data: {profile_picture_data[:60]}...")  # Print first 60 chars
        else:
            from django.templatetags.static import static
            profile_picture_data = static('default_profile.png')
    except Exception as e:
        from django.templatetags.static import static
        profile_picture_data = static('default_profile.png')
        print(f"Error getting profile picture: {str(e)}")
    return render(request, 'profile.html', {
        'username': request.user.username,
        'email': email,
        'profile_picture': profile_picture_data
    })

@login_required
def edit_profile(request):
    user = request.user
    error = None
    success = None
    if request.method == 'POST':
        # Only allow profile picture update for now
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            try:
                print(f"Uploading profile picture: {profile_picture.name}, Size: {profile_picture.size}")
                image_bytes = profile_picture.read()
                print(f"Image bytes size: {len(image_bytes)}")
                user.set_profile_picture(image_bytes)
                user.save()
                # Redirect to profile page after successful update
                return redirect('profile')
            except Exception as e:
                print(f"Error saving profile picture: {str(e)}")
                error = f'Failed to update profile picture: {str(e)}'
        else:
            error = 'No profile picture selected.'
    # Prepare current profile picture for preview
    try:
        profile_picture_bytes = user.get_profile_picture()
        print(f"Edit profile picture: {profile_picture_bytes is not None}, Type: {type(profile_picture_bytes) if profile_picture_bytes else None}")
        if profile_picture_bytes:
            import base64
            profile_picture_data = "data:image/png;base64," + base64.b64encode(profile_picture_bytes).decode('utf-8')
            print(f"Edit Base64 image data: {profile_picture_data[:60]}...")  # Print first 60 chars
        else:
            # If no profile picture, use static default
            from django.templatetags.static import static
            profile_picture_data = static('default_profile.png')
    except Exception as e:
        from django.templatetags.static import static
        profile_picture_data = static('default_profile.png')
        print(f"Error getting profile picture in edit view: {str(e)}")
    return render(request, 'edit_profile.html', {
        'username': user.username,
        'email': user.get_email(),
        'profile_picture': profile_picture_data,
        'error': error,
        'success': success
    })