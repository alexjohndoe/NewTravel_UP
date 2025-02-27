from django import forms
from .models import Testimonial, ContactRequest
from .models import CustomUser

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['rating', 'comment', 'service_used']  # Changed from 'service' to 'service_used'
        labels = {
            'service_used': 'Select Tour',
            'rating': 'Your Rating (1-5)'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'message']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']
