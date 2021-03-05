# Generated by Django 3.1.7 on 2021-03-05 18:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_car_make'),
        ('Travels', '0009_auto_20210305_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=27)),
            ],
        ),
        migrations.RenameField(
            model_name='ride',
            old_name='EndDate',
            new_name='createdOn',
        ),
        migrations.RenameField(
            model_name='ride',
            old_name='StartDate',
            new_name='endDate',
        ),
        migrations.RenameField(
            model_name='ride',
            old_name='EndingPoint',
            new_name='endingPoint',
        ),
        migrations.RenameField(
            model_name='ride',
            old_name='Price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='ride',
            old_name='StartingPoint',
            new_name='startingPoint',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='Driver',
        ),
        migrations.AddField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Driver_type', to='User.usercar'),
        ),
        migrations.AddField(
            model_name='ride',
            name='startDate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdOn', models.DateField()),
                ('requestStatusID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Travels.requeststatus')),
                ('rideId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Travels.ride')),
                ('riderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
    ]