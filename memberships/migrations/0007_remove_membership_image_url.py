# Generated by Django 3.2.14 on 2022-08-01 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0006_alter_membership_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='image_url',
        ),
    ]