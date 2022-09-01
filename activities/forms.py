
from django import forms
from .models import Activity


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
            'booking_slot_limit': 'Max Time Slots',
            'image': 'Upload a picture',
            'description': 'Description',
        }

        placeholders = {
            'activity_name': 'Activity Name',
            'booking_slot_limit': 'Max Time Slots',
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
        )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            'activity_name': 'Activity Name',
            'booking_slot_limit': 'Max Time Slots',
            'image': 'Upload a picture',
            'description': 'Description',
        }

        placeholders = {
            'activity_name': 'Activity Name',
            'booking_slot_limit': 'Max Time Slots',
            'image': 'Upload a picture',
            'description': 'Description',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
