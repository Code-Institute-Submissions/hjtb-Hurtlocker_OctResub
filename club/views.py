from django.shortcuts import render, get_object_or_404
from activities.models import Activity, Booking_Slot
from profiles.models import Profile
from django.utils import timezone


def club_page(request):
    """
    A view to return the club page
    """
    current_time = timezone.now()
    if request.user.is_authenticated:
        current_profile = get_object_or_404(Profile, user=request.user)
    else:
        current_profile = None
    try:
        profile_list = Profile.objects.all()
    except Profile.DoesNotExist:
        profile_list = []

    try:
        activity_list = Activity.objects.all()
    except Activity.DoesNotExist:
        activity_list = []

    try:
        booking_slots = Booking_Slot.objects.filter(
            end_datetime__gte=current_time
            ).order_by('end_datetime')
    except Booking_Slot.DoesNotExist:
        booking_slots = []

    context = {
        'activity_list': activity_list,
        'profile_list': profile_list,
        'current_profile': current_profile,
        'booking_slots': booking_slots,
        }

    return render(request, 'club/club_page.html', context)
