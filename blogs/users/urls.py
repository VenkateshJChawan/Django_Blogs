from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_details/', views.user_details, name='user_details'),
    path('login/', views.user_login, name='login')
]