from django import forms
from profiles.models import Profile
from profiles.widgets import CustomClearableFileInput

class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
            'is_subscribed',
            'subscription_end',
            'stripe_customer_id',
            'stripe_subscription_id',
        )

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
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
            'email': 'Email',
        }

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'image': 'Upload a profile picture',
            'is_subscribed': 'Membership',
            'phone_number': 'Phone Number',
            'email': 'Email',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
   
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.HiddenInput()