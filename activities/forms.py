from django import forms
from .models import Activity, Booking_Slot


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = (
            'id',
        )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            'activity_name': 'Activity Name',
            'image': 'Upload a picture',
            'description': 'Description',
        }

        placeholders = {
            'activity_name': 'Activity Name',
            'image': 'Upload a picture',
            'description': 'Description',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]


class EditActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = (
            'id',
            'activity_name'
        )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            'image': 'Upload a picture',
            'description': 'Description',
        }

        placeholders = {
            'image': 'Upload a picture',
            'description': 'Description',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]


class BookingSlotForm(forms.ModelForm):
    class Meta:
        model = Booking_Slot
        exclude = (
            'id',
            'end_datetime',
        )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            'activity': 'Activity',
            'day': 'Day',
            'start_hour': 'Start Hour',
            'duration': 'Duration (Hours)',
        }

        placeholders = {
            'activity': 'Activity',
            'day': 'Day',
            'start_hour': 'Start Hour',
            'duration': 'Duration',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]

        super(BookingSlotForm, self).__init__(*args, **kwargs)
        self.fields['activity'].widget = forms.HiddenInput()
