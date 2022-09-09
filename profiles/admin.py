from django.contrib import admin
from .models import Profile


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'id',
        'is_subscribed',
        'first_name',
        'last_name',
        'email',
        'subscription_end',
        'image',
    )

admin.site.register(Profile, ProfileAdmin)
