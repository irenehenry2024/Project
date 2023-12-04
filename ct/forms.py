# forms.py
from django import forms
from .models import Feedback  # Import the Feedback model

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['professional_type', 'feedback_message']



# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['professional_type', 'professional_id', 'feedback_message']


# from django import forms
# from .models import Feedback, DietitianProfile, DoctorProfile

# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['professional_type', 'professional_id', 'feedback_message']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['professional_type'].widget = forms.HiddenInput()
#         self.fields['professional_id'].widget = forms.HiddenInput()

#     def clean(self):
#         cleaned_data = super().clean()
#         professional_type = cleaned_data.get('professional_type')
#         professional_id = cleaned_data.get('professional_id')

#         if professional_type and professional_id:
#             if professional_type == 'doctor' and not DoctorProfile.objects.filter(id=professional_id).exists():
#                 self.add_error('professional_id', 'Invalid doctor selected.')
#             elif professional_type == 'dietitian' and not DietitianProfile.objects.filter(id=professional_id).exists():
#                 self.add_error('professional_id', 'Invalid dietitian selected.')

#         return cleaned_data



