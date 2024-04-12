from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import BlogAPIView, BlogSearchAPIView

router = DefaultRouter()
router.register(r'blogs', views.BlogViewSet)

urlpatterns = [
    path('create/', views.create_blog, name='create_blog'), 
    path('list/', views.blog_list, name='blog_list'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    path('<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),

    #REST APIs
    path('sm-blogs/', BlogAPIView.as_view(), name='blog_list_get'),
    path('sm-blogs/<int:pk>/', BlogAPIView.as_view(), name='blog_list_get_detail'),
    path('sm-search/', BlogSearchAPIView.as_view(), name='search_blog'),
] + router.urls