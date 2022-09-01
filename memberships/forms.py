
from django import forms
from profiles.models import Profile

class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
            'email',
            'signup_date',
            'subscription_end',
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
            'is_subscribed': 'Membership',
            'phone_number': 'Phone Number',
        }

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'image': 'Upload a profile picture',
            'is_subscribed': 'Membership',
            'phone_number': 'Phone Number',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
