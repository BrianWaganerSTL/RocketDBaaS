# Generated by Django 2.1.1 on 2018-12-03 04:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0011_auto_20181126_0131'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetricsPingDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dttm', models.DateTimeField(auto_now_add=True)),
                ('ping_db_status', models.CharField(choices=[('Normal', 'Normal'), ('Critical', 'Critical'), ('Blackout', 'Blackout')], default='', max_length=30)),
                ('ping_db_response_ms', models.IntegerField(default=0)),
                ('error_cnt', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('error_msg', models.CharField(default='', max_length=500)),
                ('server_id', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='dbaas.Server')),
            ],
            options={
                'db_table': 'metrics_ping_db',
            },
        ),
        migrations.CreateModel(
            name='MetricsPingServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dttm', models.DateTimeField(auto_now_add=True)),
                ('ping_status', models.CharField(choices=[('Normal', 'Normal'), ('Critical', 'Critical'), ('Blackout', 'Blackout')], default='', max_length=30)),
                ('ping_response_ms', models.IntegerField(default=0)),
                ('error_cnt', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('error_msg', models.CharField(default='', max_length=500)),
                ('server_id', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='dbaas.Server')),
            ],
            options={
                'db_table': 'metrics_ping_server',
            },
        ),
        migrations.RemoveField(
            model_name='metricsdbping',
            name='server_id',
        ),
        migrations.AlterField(
            model_name='metricscpu',
            name='created_dttm',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='metricsmountpoint',
            name='created_dttm',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterModelTable(
            name='metricsmountpoint',
            table='metrics_mount_point',
        ),
        migrations.DeleteModel(
            name='MetricsDbPing',
        ),
    ]