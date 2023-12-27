# Generated by Django 4.0.4 on 2023-12-24 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='method_of_treatment',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_type',
            field=models.CharField(blank=True, choices=[('Home', 'Home'), ('Clinic', 'Clinic')], default=None, max_length=255, null=True),
        ),
    ]