# Generated by Django 4.2.5 on 2023-11-22 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0054_timeslot_dietitian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='dietitian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
