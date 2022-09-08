from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Activity, Booking_Slot, Booking
from profiles.models import Profile
from profiles.views import user_subscription_check, user_is_staff_check
from .forms import ActivityForm, EditActivityForm, BookingSlotForm
import datetime as dt
import pytz
from django.utils import timezone


@user_passes_test(user_subscription_check, login_url='/memberships/membership_signup')
@login_required
def all_activities(request):
    """A view to show all activities"""
    current_user = request.user
    current_profile = get_object_or_404(Profile, user=current_user)

    try:
        activity_list = Activity.objects.all()

    except Activity.DoesNotExist:
        activity_list = []

    context = {
        'current_profile': current_profile,
        'current_user': current_user,
        'activity_list': activity_list
        }

    return render(request, 'activities/all_activities.html', context)


@user_passes_test(user_subscription_check, login_url='/memberships/membership_signup')
@login_required
def activity_page(request, key):
    """
    A view to return the activity page
    """
    current_user = request.user
    current_activity = get_object_or_404(Activity, pk=key)
    current_profile = get_object_or_404(Profile, user=current_user)
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
        'current_profile': current_profile,
        'current_user': current_user,
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
    current_profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES,)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'New Activity Created Successfully')
            except Exception as e:
                messages.error(
                    request, """
                    Sorry, something went wrong while
                    trying to create the activity.
                    """
                )
                return HttpResponse(content=e, status=400)
            return redirect('/activities')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')
    else:
        form = ActivityForm()

    context = {
        'form': form,
        'current_profile': current_profile,
        }

    return render(request, 'activities/add_activity.html', context)


@user_passes_test(user_is_staff_check, login_url='/memberships/membership_signup')
@login_required
def edit_activity(request, key):
    """
    A view to allow admins edit actvities
    """
    current_profile = get_object_or_404(Profile, user=request.user)
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
            try:
                form.save()
                messages.success(request, 'Activity Updated Successfully')
            except Exception as e:
                messages.error(
                    request, """
                    Sorry, something went wrong while
                    trying to update the activity.
                    """
                )
                return HttpResponse(content=e, status=400)
            return redirect('activity_page', current_activity.id)
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')
    else:
        form = EditActivityForm(instance=current_activity)

    context = {
        'current_profile': current_profile,
        'current_activity': current_activity,
        'form': form,
        'slots': slots,
        }
    return render(request, 'activities/edit_activity.html', context)


@user_passes_test(user_is_staff_check, login_url='../memberships/membership_signup')
@login_required
def delete_activity(request, key):
    """
    A view to allow staff delete booking slots for activities
    """

    activity_to_be_deleted = get_object_or_404(Activity, pk=key)
    current_activity_id = activity_to_be_deleted.id

    try:
        activity_to_be_deleted.delete()
        messages.success(request, 'Activity Deleted Successfully')
    except Exception as e:
        messages.error(
            request, """
            Sorry, something went wrong while
            trying to delete this activity.
            """
        )
        return HttpResponse(content=e, status=400)
    return redirect('activity_page', current_activity_id)


@user_passes_test(user_is_staff_check, login_url='/memberships/membership_signup')
@login_required
def add_booking_slot(request, key):
    """
    A view to allow admins create booking slots for activities
    """
    current_activity = get_object_or_404(Activity, pk=key)
    current_profile = get_object_or_404(Profile, user=request.user)

    try:
        existing_slots = Booking_Slot.objects.filter(
            activity=current_activity.activity_name
            )
    except Booking_Slot.DoesNotExist:
        existing_slots = []

    current_datetime = dt.datetime.now()
    datetimes_of_next_week = {}

    for x in range(1, 8):
        future_datetime = current_datetime + dt.timedelta(days=x)
        day_of_week = future_datetime.weekday()
        datetimes_of_next_week[day_of_week] = future_datetime

    if request.method == 'POST':
        form = BookingSlotForm(request.POST)
        if form.is_valid():
            new_booking_slot = form.instance
            new_booking_slot_date = datetimes_of_next_week[new_booking_slot.day].date()
            new_booking_slot_start_time = new_booking_slot.start_hour
            new_booking_slot_start_datetime = dt.datetime.combine(
                new_booking_slot_date, new_booking_slot_start_time
                )
            new_booking_slot_start_seconds = new_booking_slot_start_datetime.timestamp()
            new_booking_slot_duration_seconds = new_booking_slot.duration.seconds
            new_booking_slot_end = new_booking_slot_start_seconds + new_booking_slot_duration_seconds
            new_booking_slot_end_datetime = dt.datetime.fromtimestamp(new_booking_slot_end)
            new_booking_slot.end_datetime = new_booking_slot_end_datetime

            overlap = False

            for existing_booking_slot in existing_slots:
                existing_start = (
                    existing_booking_slot.end_datetime - existing_booking_slot.duration
                    )
                existing_end = existing_booking_slot.end_datetime
                utc = pytz.UTC
                new_start = utc.localize(new_booking_slot_start_datetime)
                new_end = utc.localize(new_booking_slot_end_datetime)
                if (
                    existing_start <= new_start < existing_end or
                    existing_start < new_end <= existing_end
                ):
                    overlap = True

            if overlap is True:
                messages.error(
                    request, 'A booking slot already exists at this time!'
                )
            else:
                try:
                    form.save()
                    messages.success(
                        request, 'New Booking Slot Created Successfully'
                        )
                except Exception as e:
                    messages.error(
                        request, """
                        Sorry, something went wrong while
                        trying to create this booking slot.
                        """
                    )
                    return HttpResponse(content=e, status=400)

                return redirect('edit_activity', current_activity.id)
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
        'current_activity': current_activity,
        'current_profile': current_profile
        }

    return render(request, 'activities/add_booking_slot.html', context)


@user_passes_test(user_is_staff_check, login_url='../memberships/membership_signup')
@login_required
def delete_booking_slot(request, key):
    """
    A view to allow staff delete booking slots for activities
    """

    booking_slot_to_be_deleted = get_object_or_404(Booking_Slot, pk=key)
    current_activity = booking_slot_to_be_deleted.activity
    try:
        booking_slot_to_be_deleted.delete()
        messages.success(request, 'Booking Slot Deleted Successfully')
    except Exception as e:
        messages.error(
            request, """
            Sorry, something went wrong while
            trying to delete this booking slot.
            """
        )
        return HttpResponse(content=e, status=400)
    return redirect('edit_activity', current_activity.id)


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

    current_activity = current_booking_slot.activity
    new_booking_start_hour = current_booking_slot.start_hour
    new_booking_end_datetime = current_booking_slot.end_datetime

    new_booking = Booking(
        booking_slot_used=current_booking_slot,
        member=current_profile,
        booking_start_time=new_booking_start_hour,
        booking_end_time=new_booking_end_datetime,
        )

    overlap = False
    for member_booking in members_bookings:
        if current_booking_slot.id == member_booking.booking_slot_used.id:
            messages.error(
                request, "You've already booked this slot."
            )
        existing_booking_slot = member_booking.booking_slot_used
        existing_start = (
            existing_booking_slot.end_datetime - current_booking_slot.duration
            )
        existing_end = existing_booking_slot.end_datetime

        new_booking_date = new_booking_end_datetime.date()
        new_booking_start_datetime = dt.datetime.combine(
            new_booking_date, new_booking_start_hour
            )
        utc = pytz.UTC
        new_start = utc.localize(new_booking_start_datetime)
        new_end = new_booking_end_datetime
        if (
            existing_start <= new_start < existing_end or
            existing_start < new_end <= existing_end
        ):
            overlap = True

    if overlap is True:
        messages.error(
            request, 'You already have a booking at this time!'
        )
    else:
        try:
            new_booking.save()
            messages.success(
                request, f"""
                You've booked {current_booking_slot.activity.activity_name}
                on {new_booking_end_datetime.strftime("%d/%m")}.
                """
                )
        except Exception as e:
            messages.error(
                request, """
                Sorry, something went wrong while trying to make this booking.
                """
                )
            return HttpResponse(content=e, status=400)
                
    return redirect('activity_page', current_activity.id)
