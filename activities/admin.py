from django.contrib import admin
from .models import Activity, Booking_Slot, Booking


# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'activity_name',
        'description',
    )


class Booking_SlotAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'activity',
        'day',
        'start_hour',
        'duration',
    )


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member',
        'booking_slot_used',
    )


admin.site.register(Activity, ActivityAdmin,)
admin.site.register(Booking_Slot, Booking_SlotAdmin,)
admin.site.register(Booking, BookingAdmin,)
