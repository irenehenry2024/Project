# Generated by Django 4.2.5 on 2023-11-03 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0037_rename_intake_date_foodintake_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bmi',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]