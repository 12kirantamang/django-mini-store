from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),
    
    # Use custom logout view
    path('logout/', views.custom_logout, name='logout'),

    path('signup/', views.signup, name='signup'),
]