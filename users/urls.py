from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import login_view
from .views import home_view
from .views import register_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
]
