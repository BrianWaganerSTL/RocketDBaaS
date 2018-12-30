# Generated by Django 2.1.4 on 2018-12-30 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='closed_dttm',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='note',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='note_by',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='ticket',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='incidentnotification',
            name='acknowledged_by',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='incidentnotification',
            name='acknowledged_dttm',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='thresholdtest',
            name='detail_element',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
