from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
# from activities.models import Booking


class Profile(models.Model):
    """User profile model"""

    id = models.BigAutoField(primary_key=True)
    is_subscribed = models.BooleanField(default=False)
    # possibly change email to be reference field on the user - https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.to_field
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    signup_date = models.DateTimeField(auto_now_add=True)
    subscription_end = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    # bookings = models.ManyToManyField(Booking, blank=True)

    # Stripe Customer Fields
    stripe_customer_id = models.CharField(
        max_length=255, null=True, blank=True)
    stripe_subscription_id = models.CharField(
        max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    # Taken from Boutique Ado tutorial
    @receiver(post_save, sender=User)
    def create_or_update_profile(sender, instance, created, **kwargs):
        """
        Create or update the user profile
        """
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
