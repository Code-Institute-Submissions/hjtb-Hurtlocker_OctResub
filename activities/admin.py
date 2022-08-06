from django.contrib import admin
from .models import Activity


# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )

admin.site.register(Activity, ActivityAdmin)