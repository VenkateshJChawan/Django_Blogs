from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_blog, name='create_blog'), 
    path('list/', views.blog_list, name='blog_list'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
]