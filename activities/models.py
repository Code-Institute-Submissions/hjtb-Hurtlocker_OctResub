from django.db import models

# Create your models here.


class Activity(models.Model):

    class Meta:
        verbose_name_plural = 'Activities'
        
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)