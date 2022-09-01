from django.db import models


class Activity(models.Model):
    """Activity model to hold information regarding activities"""

    class Meta:
        verbose_name_plural = 'Activities'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Booking_Slot(models.Model):
    """Booking Slot model to store booking slots"""

    id = models.BigAutoField(primary_key=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=False, null=True)
    duration = models.DurationField(max_length=255, null=True)

    def __str__(self):
        return str(self.id)


# class Booking(models.Model):
#     """Booking model to hold information regarding bookings"""

#     id = models.BigAutoField(primary_key=True)
#     booking_slot = models.ForeignKey(Booking_Slot, on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.id)
