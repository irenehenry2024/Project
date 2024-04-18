from django.apps import AppConfig


class CtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ct'

from django.apps import AppConfig
import nltk

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'

    def ready(self):
        # Download NLTK resources when Django starts
        nltk.download('punkt')