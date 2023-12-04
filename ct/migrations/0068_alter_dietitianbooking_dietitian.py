# Generated by Django 4.2.5 on 2023-12-03 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0067_alter_dietitianbooking_dietitian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dietitianbooking',
            name='dietitian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dietitian_bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]