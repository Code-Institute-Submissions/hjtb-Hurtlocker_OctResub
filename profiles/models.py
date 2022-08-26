from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from activities.models import Activity

# Create your models here.


class Profile(models.Model):
    """User profile model"""

    id = models.BigAutoField(primary_key=True)
    membership = models.ForeignKey(
        'memberships.Membership', on_delete=models.PROTECT, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(max_length=300, blank=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True)
    activities = models.ManyToManyField(Activity)

    # billing information
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)

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
