from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm
from .models import Blog

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', blog_id=blog_id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})

def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        blog.delete()
    return redirect('blog_list')


# REST APIs using DRF
from rest_framework import viewsets
from .serializers import BlogSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


# Seperate methods for each request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BlogAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            try:
                blog = Blog.objects.get(pk=pk)
                serializer = BlogSerializer(blog)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Blog.DoesNotExist:
                return Response({'error':'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            blogs = Blog.objects.all().order_by('id')
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        data = request.data
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Blog created successfully', 'blog':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Blog updated successfully', 'blog' : serializer.data} , status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
                return Response({'error':'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Blog updated successfully', 'blog' : serializer.data} , status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
                return Response({'error':'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
            blog.delete()
            return Response({'message': 'Blog deleted successfully'} ,status=status.HTTP_204_NO_CONTENT)
        except Blog.DoesNotExist:
            return Response({'error':'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        
from django.db.models import Q 

class BlogSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')

        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

        serializer = BlogSerializer(blogs, many=True)

        return Response({
            'message': 'Search results found',
            'count': blogs.count(),
            'blogs': serializer.data
        }, status=status.HTTP_200_OK)