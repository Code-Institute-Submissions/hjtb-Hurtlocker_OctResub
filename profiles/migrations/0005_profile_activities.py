# Generated by Django 3.2.14 on 2022-08-06 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
        ('profiles', '0004_auto_20220801_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activities',
            field=models.ManyToManyField(to='activities.Activity'),
        ),
    ]