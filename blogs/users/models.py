from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)  # YYYY-MM-DD
    about = models.TextField(blank=True)
    city = models.CharField(max_length=25, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = slugify(self.email.split('@')[0])   # venkatesh@gmail.com

            # Ensure uniqueness of generated username
            base_username = self.username
            count = 1
            while CustomUser.objects.filter(username = self.username).exists():
                self.username = f"{base_username}{count}"             # venkatesh1
                count += 1

        super().save(*args, **kwargs)



