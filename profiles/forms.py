from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
            'signup_date',
            'subscription_end',
            'is_subscribed',
            'stripe_customer_id',
            'stripe_subscription_id',
        )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'image': 'Upload a profile picture',
            'phone_number': 'Phone Number',
            'email': 'Email',
        }

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'image': 'Upload a profile picture',
            'phone_number': 'Phone Number',
            'email': 'Email',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.HiddenInput()
