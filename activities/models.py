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
            (0, 'Mon'), (1, 'Tue'), (2, 'Wed'),
            (3, 'Thur'), (4, 'Fri'), (5, 'Sat'),
            (6, 'Sun'),
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
    duration = models.DurationField(
        null=False, blank=False, default=dt.timedelta(hours=1),
        choices=DURATION_CHOICES
        )
    start_hour = models.TimeField(auto_now_add=False, choices=HOUR_CHOICES,)
    end_datetime = models.DateTimeField(
        auto_now_add=False, blank=True, null=True
        )

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
    booking_start_time = models.TimeField(
        auto_now_add=False, blank=True, null=True
        )
    booking_end_time = models.DateTimeField(
        auto_now_add=False, blank=True, null=True
        )

    def __str__(self):
        return str(self.id)
