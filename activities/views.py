from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Activity, Booking_Slot, Booking
from profiles.models import Profile
from profiles.views import user_subscription_check, user_is_staff_check
from .forms import ActivityForm, EditActivityForm, BookingSlotForm
import datetime as dt
from django.utils import timezone


@user_passes_test(user_subscription_check, login_url='/memberships/membership_signup')
@login_required
def all_activities(request):
    """A view to show all activities"""

    try:
        activity_list = Activity.objects.all()

    except Activity.DoesNotExist:
        activity_list = []

    context = {'activity_list': activity_list}

    return render(request, 'activities/all_activities.html', context)


@user_passes_test(user_subscription_check, login_url='/memberships/membership_signup')
@login_required
def activity_page(request, key):
    """
    A view to return the activity page
    """
    current_activity = get_object_or_404(Activity, pk=key)
    current_profile = get_object_or_404(Profile, user=request.user)
    current_datetime = timezone.now()
    slots_already_used = []

    try:
        members_bookings = Booking.objects.filter(
            member=current_profile, booking_end_time__gte=current_datetime
            ).order_by('booking_end_time')
    except Booking.DoesNotExist:
        members_bookings = []

    try:
        booking_slots = Booking_Slot.objects.filter(
            activity=current_activity.activity_name
            ).order_by('end_datetime')

    except Booking_Slot.DoesNotExist:
        booking_slots = []

    for members_booking in members_bookings:
        for booking_slot in booking_slots:
            if booking_slot.id == members_booking.booking_slot_used.id:
                slots_already_used.append(booking_slot.id)

    context = {
        'current_activity': current_activity,
        'booking_slots': booking_slots,
        'members_bookings': members_bookings,
        'current_datetime': current_datetime,
        'slots_already_used': slots_already_used,
        }
    return render(request, 'activities/activity_page.html', context)


@user_passes_test(user_is_staff_check, login_url='/memberships/membership_signup')
@login_required
def add_activity(request):
    """
    A view to allow admins add actvities
    """

    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES,)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Activity Created Successfully')
            return redirect('/activities')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')
    else:
        form = ActivityForm()

    context = {'form': form}

    return render(request, 'activities/add_activity.html', context)


@user_passes_test(user_is_staff_check, login_url='/memberships/membership_signup')
@login_required
def edit_activity(request, key):
    """
    A view to allow admins edit actvities
    """

    current_activity = get_object_or_404(Activity, pk=key)

    try:
        slots = Booking_Slot.objects.filter(
            activity=current_activity.activity_name
            )

    except Booking_Slot.DoesNotExist:
        slots = []

    if request.method == 'POST':
        form = EditActivityForm(
            request.POST, request.FILES, instance=current_activity
            )
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity Updated Successfully')
            return redirect('/activities')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')
    else:
        form = EditActivityForm(instance=current_activity)

    context = {
        'current_activity': current_activity,
        'form': form,
        'slots': slots,
        }
    return render(request, 'activities/edit_activity.html', context)


@user_passes_test(user_is_staff_check, login_url='/memberships/membership_signup')
@login_required
def add_booking_slot(request, key):
    """
    A view to allow admins create booking slots for activities
    """
    current_activity = get_object_or_404(Activity, pk=key)

    current_datetime = dt.datetime.now()
    datetimes_of_next_week = {}

    for x in range(1, 8):
        future_datetime = current_datetime + dt.timedelta(days=x)
        day_of_week = future_datetime.weekday()
        datetimes_of_next_week[day_of_week] = future_datetime

    if request.method == 'POST':
        form = BookingSlotForm(request.POST)
        if form.is_valid():
            booking = form.instance
            booking_date = datetimes_of_next_week[booking.day].date()
            booking_start_time = booking.start_hour
            booking_start_datetime = dt.datetime.combine(
                booking_date, booking_start_time
                )
            booking_start_seconds = booking_start_datetime.timestamp()
            booking_duration_seconds = booking.duration.seconds
            booking_end = booking_start_seconds + booking_duration_seconds
            booking_end_datetime = dt.datetime.fromtimestamp(booking_end)
            booking.end_datetime = booking_end_datetime
            form.save()
            messages.success(request, 'New Booking Slot Created Successfully')
            return redirect('activity_page', current_activity.id)
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')
    else:
        form = BookingSlotForm(
            initial={
                'activity': current_activity,
            },
        )

    context = {
        'form': form,
        'current_activity': current_activity
        }

    return render(request, 'activities/add_booking_slot.html', context)


@user_passes_test(user_is_staff_check, login_url='/memberships/membership_signup')
@login_required
def edit_booking_slot(request, key):
    """
    A view to allow admins edit booking slots for activities
    """

    current_slot = get_object_or_404(Booking_Slot, pk=key)
    current_activity = current_slot.activity

    if request.method == 'POST':
        form = BookingSlotForm(request.POST, instance=current_slot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking Slot Updated Successfully')
            return redirect('activity_page', current_activity.id)
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')
    else:
        form = BookingSlotForm(instance=current_slot)

    context = {
        'current_activity': current_activity,
        'current_slot': current_slot,
        'form': form,
        }
    return render(request, 'activities/edit_booking_slot.html', context)


@user_passes_test(user_subscription_check, login_url='/memberships/membership_signup')
@login_required
def create_booking(request, key):
    """
    A view to allow members make bookings
    """
    current_booking_slot = get_object_or_404(Booking_Slot, pk=key)
    current_profile = get_object_or_404(Profile, user=request.user)
    current_time = timezone.now()

    try:
        members_bookings = Booking.objects.filter(
            member=current_profile, booking_end_time__gte=current_time
            ).order_by('booking_end_time')
    except Booking.DoesNotExist:
        members_bookings = []

    for members_booking in members_bookings:
        if current_booking_slot.id == members_booking.booking_slot_used.id:
            messages.error(
            request, "You've already booked this slot."
            )
            return redirect('activity_page', current_booking_slot.activity.id)

    current_activity = current_booking_slot.activity
    start_time = current_booking_slot.start_hour
    end_time = current_booking_slot.end_datetime

    new_booking = Booking(
        booking_slot_used=current_booking_slot,
        member=current_profile,
        booking_start_time=start_time,
        booking_end_time=end_time,
        )

    new_booking.save()
    messages.success(request, 'New Booking Slot Created Successfully')

    return redirect('activity_page', current_activity.id)
