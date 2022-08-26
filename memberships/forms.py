
from django import forms
from profiles.models import Profile

class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
            'signup_date',
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
            'bio': 'Bio',
            'image': 'Upload a profile picture',
            'is_subscribed': 'Membership',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'city': 'City',
            'county': 'County',
            'postcode': 'Postcode',
        }

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'bio': 'Bio',
            'image': 'Upload a profile picture',
            'is_subscribed': 'Membership',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'city': 'City',
            'county': 'County',
            'postcode': 'Postcode',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
