# Generated by Django 4.2.5 on 2023-10-30 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0027_doctorprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]