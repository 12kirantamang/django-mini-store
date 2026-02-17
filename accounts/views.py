from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'accounts/signup.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # AUTO-LOGIN after signup
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}!")
            
            # Redirect to checkout or home
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        
        return redirect('login')
    
    return render(request, 'accounts/signup.html')
def logout_success(request):
    return render(request, 'accounts/logout.html')

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout_confirm.html'
    http_method_names = ['get', 'post']

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home') 