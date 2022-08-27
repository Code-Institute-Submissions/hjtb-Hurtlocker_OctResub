from django.contrib import admin
from .models import Profile


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_subscribed',
        'user',
        'first_name',
        'last_name',
        'email',
        'bio',
        'signup_date',
        'image',
    )

admin.site.register(Profile, ProfileAdmin)