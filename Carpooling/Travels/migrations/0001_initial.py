# Generated by Django 3.1.7 on 2021-03-07 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=27)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startingPoint', models.CharField(max_length=25)),
                ('endingPoint', models.CharField(default=1, max_length=25)),
                ('price', models.IntegerField(default=1)),
                ('createdOn', models.DateField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('driver', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Driver_type', to='User.usercar')),
            ],
        ),
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdOn', models.DateField()),
                ('requestStatusID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Travels.requeststatus')),
                ('rideId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Travels.ride')),
                ('riderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
