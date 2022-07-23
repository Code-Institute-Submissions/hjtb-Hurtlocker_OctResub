from django.db import models

# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)


    # id = models.BigAutoField(primary_key=True)
    # username = models.CharField(max_length=30)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    # bio = models.TextField(max_length=255, blank=True)
    # signup_date = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(blank=True)

    def __str__(self):
        return str(self.name)