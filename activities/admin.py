from django.contrib import admin
from .models import Activity, Booking_Slot


# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )


class Booking_SlotAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'activity_id',
        'start_time',
        'duration',
    )


# class BookingAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'booking_slot',
#     )


admin.site.register(Activity, ActivityAdmin,)
admin.site.register(Booking_Slot, Booking_SlotAdmin,)
# admin.site.register(Booking, BookingAdmin,)
