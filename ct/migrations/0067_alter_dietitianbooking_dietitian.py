# Generated by Django 4.2.5 on 2023-12-02 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0066_dietitianbooking_amount_dietitianbooking_session_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dietitianbooking',
            name='dietitian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dietitian_bookings', to='ct.dietitianprofile'),
        ),
    ]
