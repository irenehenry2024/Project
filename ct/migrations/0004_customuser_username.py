# Generated by Django 4.2.5 on 2023-09-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0003_remove_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]