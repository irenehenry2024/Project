# Generated by Django 4.2.5 on 2023-10-27 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0024_userprofile_height_userprofile_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
