from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Activity, Booking_Slot
from profiles.models import Profile
from .forms import ActivityForm, EditActivityForm, BookingSlotForm


def all_activities(request):
    """A view to show all activities"""

    try:
        activity_list = Activity.objects.all()

    except Activity.DoesNotExist:
        activity_list = []

    context = {'activity_list': activity_list}

    return render(request, 'activities/all_activities.html', context)


def activity_page(request, key):
    """
    A view to return the activity page
    """

    current_activity = get_object_or_404(Activity, pk=key)

    context = {
        'current_activity': current_activity,
        }
    return render(request, 'activities/activity_page.html', context)


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


def edit_activity(request, key):
    """
    A view to allow admins edit actvities
    """

    current_activity = get_object_or_404(Activity, pk=key)

    try:
        slots = Booking_Slot.objects.filter(activity=current_activity.activity_name)

    except Booking_Slot.DoesNotExist:
        slots = []

    if request.method == 'POST':
        form = EditActivityForm(request.POST, instance=current_activity)
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


def add_booking_slot(request, key):
    """
    A view to allow admins create booking slots for activities
    """
    current_activity = get_object_or_404(Activity, pk=key)

    if request.method == 'POST':
        form = BookingSlotForm(request.POST)
        if form.is_valid():
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
