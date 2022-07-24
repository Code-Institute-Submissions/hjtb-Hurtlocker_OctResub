from django.db import models

# Create your models here.


class Activity(models.Model):
    """Activity model to hold information regarding activities"""

    class Meta:
        verbose_name_plural = 'Activities'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)