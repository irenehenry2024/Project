# Generated by Django 4.2.5 on 2023-11-05 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0039_alter_booking_booking_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=100)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
