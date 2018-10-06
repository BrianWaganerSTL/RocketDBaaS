# Generated by Django 2.1.1 on 2018-10-05 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0014_auto_20181003_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusternote',
            name='created_by',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='clusternote',
            name='note_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('Success', 'Success'), ('Danger', 'Danger'), ('Warning', 'Warning'), ('Info', 'Info'), ('Light', 'Light'), ('Dark', 'Dark')], max_length=15, null=True),
        ),
    ]
