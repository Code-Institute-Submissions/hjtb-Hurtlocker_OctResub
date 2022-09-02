from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Activity, Booking_Slot
from profiles.models import Profile
from .forms import ActivityForm, EditActivityForm, BookingSlotForm


def all_activities(request):
    """A view to show all activities"""

    activity_list = get_list_or_404(Activity)

    context = {'activity_list': activity_list}

    return render(request, 'activities/all_activities.html', context)


def activity_page(request, key):
    """
    A view to return the activity page
    """

    current_activity = get_object_or_404(Activity, pk=key)

    try:
        slots = Booking_Slot.objects.filter(activity=current_activity.activity_name)

    except Booking_Slot.DoesNotExist:
        slots = []
        
    context = {
        'current_activity': current_activity,
        'slots': slots,
        }
    return render(request, 'activities/activity_page.html', context)


def add_activity(request):
    """
    A view to allow admins add actvities
    """
    form = ActivityForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'New Activity Created Successfully')
            return redirect('/activities')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')

    context = {'form': form}

    return render(request, 'activities/add_activity.html', context)


def edit_activity(request, key):
    """
    A view to allow admins edit actvities
    """
    try:
        current_activity = get_object_or_404(Activity, pk=key)
        form = EditActivityForm(request.POST, instance=current_activity)
    except Exception as e:
        print(e)
        return JsonResponse({'error': (e.args[0])}, status=403)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity Updated Successfully')
            return redirect('/activities')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')

    context = {
        'current_activity': current_activity,
        'form': form,
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
    A view to allow admins edit actvities
    """
    try:
        current_activity = get_object_or_404(Activity, pk=key)
        form = ActivityForm(request.POST, instance=current_activity)

    except Exception as e:
        print(e)
        return JsonResponse({'error': (e.args[0])}, status=403)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity Updated Successfully')
            return redirect('/activities')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')

    context = {
        'current_activity': current_activity,
        'form': form,
        }
    return render(request, 'activities/edit_activity.html', context)
