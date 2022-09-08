from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from activities.models import Booking


class Profile(models.Model):
    """User profile model"""

    id = models.BigAutoField(primary_key=True)
    is_subscribed = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    subscription_end = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)

    # Stripe Customer Fields
    stripe_customer_id = models.CharField(
        max_length=100, null=True, blank=True)
    stripe_subscription_id = models.CharField(
        max_length=100, null=True, blank=True)

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
