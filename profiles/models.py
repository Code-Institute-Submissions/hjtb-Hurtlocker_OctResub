from django.db import models

# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)