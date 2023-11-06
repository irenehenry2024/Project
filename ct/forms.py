from django import forms
from .models import Feedback  # Import the Feedback model

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['professional_type', 'feedback_message']
