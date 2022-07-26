from django.db import models

# Create your models here.


class Membership(models.Model):
    """Membership model to hold information regarding memberships"""

    class Meta:
        verbose_name_plural = 'Activities'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)