from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """User profile model"""

    id = models.BigAutoField(primary_key=True)
    membership = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(max_length=255, blank=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return str(self.user)
