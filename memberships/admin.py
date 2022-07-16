from django.contrib import admin
from .models import Membership
from .models import Member
from .models import Activity

# Register your models here.

class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Activity, ActivityAdmin)