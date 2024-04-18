# forms.py

from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','video_file']

from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image']  # Fields to include in the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            # You may want to customize the widget for the image field if needed
        }
        labels = {
            'title': 'Title',  # Custom labels for the fields
            'description': 'Description',
            'image': 'Image',
        }






from .models import Food, Image

class FoodForm(forms.ModelForm):
    '''
    A ModelForm class for adding a new food item
    '''
    class Meta:
        model = Food
        fields = ['food_name', 'quantity', 'calories', 'fat', 'carbohydrates', 'protein', 'category']

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ImageForm(forms.ModelForm):
    '''
    A ModelForm class for adding an image to the food item
    '''
    class Meta:
        model = Image
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.visible_fields()[0].field.widget.attrs['class'] = 'form-control'



