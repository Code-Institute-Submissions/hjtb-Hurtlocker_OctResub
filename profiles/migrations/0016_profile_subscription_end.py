# Generated by Django 3.2.14 on 2022-08-31 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_remove_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscription_end',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]