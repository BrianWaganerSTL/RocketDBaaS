# Generated by Django 2.1.4 on 2018-12-07 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0022_auto_20181206_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issuenotification',
            old_name='notification_note',
            new_name='notification_body',
        ),
        migrations.RenameField(
            model_name='metricthreshold',
            old_name='clear_ticks',
            new_name='normal_ticks',
        ),
        migrations.RenameField(
            model_name='metricthreshold',
            old_name='clear_value',
            new_name='normal_value',
        ),
        migrations.RemoveField(
            model_name='issuetracker',
            name='metric_check',
        ),
        migrations.RemoveField(
            model_name='metricthreshold',
            name='clear_predicate_type',
        ),
        migrations.AddField(
            model_name='issuenotification',
            name='notification_subject',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='issuetracker',
            name='current_status',
            field=models.CharField(choices=[('Normal', 'Normal'), ('Warning', 'Warning'), ('Critical', 'Critical'), ('Blackout', 'Blackout'), ('Normal', 'Normal'), ('Unknown', 'Unknown')], default='', max_length=15),
        ),
        migrations.AddField(
            model_name='issuetracker',
            name='element_details',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='issuetracker',
            name='last_status',
            field=models.CharField(choices=[('Normal', 'Normal'), ('Warning', 'Warning'), ('Critical', 'Critical'), ('Blackout', 'Blackout'), ('Normal', 'Normal'), ('Unknown', 'Unknown')], default='', max_length=15),
        ),
        migrations.AddField(
            model_name='issuetracker',
            name='metric_threshold',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.ProtectedError, to='dbaas.MetricThreshold'),
        ),
        migrations.AddField(
            model_name='metricthreshold',
            name='normal_predicate_type',
            field=models.CharField(choices=[('>=', '>='), ('>', '>'), ('==', '=='), ('!=', '!='), ('<=', '<='), ('<', '<')], default='<', max_length=15),
        ),
        migrations.AlterField(
            model_name='metricthreshold',
            name='critical_predicate_type',
            field=models.CharField(choices=[('>=', '>='), ('>', '>'), ('==', '=='), ('!=', '!='), ('<=', '<='), ('<', '<')], default='>=', max_length=15),
        ),
        migrations.AlterField(
            model_name='metricthreshold',
            name='warning_predicate_type',
            field=models.CharField(choices=[('>=', '>='), ('>', '>'), ('==', '=='), ('!=', '!='), ('<=', '<='), ('<', '<')], default='>=', max_length=15),
        ),
    ]
