from django.db import models
from profiles.models import Profile
from django.core.validators import MaxValueValidator, MinValueValidator


class Activity(models.Model):
    """
    Activity model to hold information regarding activities
    """

    class Meta:
        verbose_name_plural = 'Activities'

    id = models.BigAutoField(primary_key=True)
    activity_name = models.CharField(max_length=255, unique=True)
    booking_slot_limit = models.IntegerField(default=3)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.activity_name)


class Booking_Slot(models.Model):
    """
    Booking Slot model to store booking slots
    """
    id = models.BigAutoField(primary_key=True)
    activity = models.ForeignKey(
        Activity, to_field='activity_name', on_delete=models.CASCADE
        )
    day = models.PositiveSmallIntegerField(
        choices=[
            (1, 'monday'), (2, 'tuesday'), (3, 'wednesday'),
            (4, 'thursday'), (5, 'friday'), (6, 'saturday'),
            (7, 'sunday')
            ],
        validators=[MaxValueValidator(7), MinValueValidator(1)]
        )
    start_hour = models.TimeField(auto_now_add=False)
    duration = models.DurationField(max_length=255, null=True)

    def __str__(self):
        return str(self.id)


class Booking(models.Model):
    """
    Booking model to hold information regarding bookings
    """
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(
        Profile, to_field='user', on_delete=models.CASCADE
        )
    booking_slot_used = models.ForeignKey(
        Booking_Slot, on_delete=models.CASCADE
        )

    def __str__(self):
        return str(self.id)
