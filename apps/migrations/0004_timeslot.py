# Generated by Django 4.2.5 on 2023-12-20 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_delete_petowner'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.CharField(max_length=255)),
                ('time', models.CharField(max_length=10)),
            ],
        ),
    ]