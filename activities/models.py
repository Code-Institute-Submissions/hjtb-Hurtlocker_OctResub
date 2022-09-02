from django.db import models
from profiles.models import Profile
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime as dt



class Activity(models.Model):
    """
    Activity model to hold information regarding activities
    """

    class Meta:
        verbose_name_plural = 'Activities'

    id = models.BigAutoField(primary_key=True)
    activity_name = models.CharField(max_length=255, unique=True)
    booking_slot_limit = models.PositiveSmallIntegerField(
        default=3, validators=[MaxValueValidator(20), MinValueValidator(1)]
        )
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.activity_name)


HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(5, 22)]
DURATION_CHOICES = [
            (dt.timedelta(hours=0.5), '30 mins'), (dt.timedelta(hours=1), '1 hour'),
            (dt.timedelta(hours=1.5), '1:30 mins'), (dt.timedelta(hours=2), '2 hours'), 
            (dt.timedelta(hours=2.5), '2:30 mins'), (dt.timedelta(hours=3), '3 hours'),
            ]
DAY_CHOICES = [
            (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
            (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'),
            (7, 'Sunday'),
            ]


class Booking_Slot(models.Model):
    """
    Booking Slot model to store booking slots
    """
    id = models.BigAutoField(primary_key=True)
    activity = models.ForeignKey(
        Activity, to_field='activity_name', on_delete=models.CASCADE
        )
    day = models.PositiveSmallIntegerField(
        choices=DAY_CHOICES,
        validators=[MaxValueValidator(7), MinValueValidator(1)]
        )
    start_hour = models.TimeField(auto_now_add=False, choices=HOUR_CHOICES,)
    duration = models.DurationField(max_length=255, default=10000, null=False, blank=False, choices=DURATION_CHOICES)

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
