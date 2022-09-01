# Generated by Django 3.2.14 on 2022-09-01 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Booking_Slot',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField(null=True)),
                ('duration', models.DurationField(max_length=255, null=True)),
                ('activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activity')),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('booking_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.booking_slot')),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
    ]
