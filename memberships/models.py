from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Membership(models.Model):
    """Membership model to hold information regarding memberships"""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    number_of_activities = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], blank=False, default=1)

    def __str__(self):
        return str(self.name)
