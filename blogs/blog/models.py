from django.db import models
from users.models import CustomUser

def blog_image_upload_path(instance, filename):
    return f'blog_images/{instance.author.id}/{filename}'  # blog_image/3/honda.jpeg

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to=blog_image_upload_path, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title