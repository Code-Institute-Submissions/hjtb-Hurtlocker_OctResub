# Generated by Django 3.2.14 on 2022-09-06 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0014_alter_booking_slot_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='booking_slot_limit',
        ),
    ]