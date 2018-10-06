# Generated by Django 2.1.1 on 2018-10-06 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0022_auto_20181004_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='read_write_port',
            field=models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, related_name='read_write_port_id', to='dbaas.ServerPort'),
        ),
        migrations.AlterField(
            model_name='restore',
            name='to_cluster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, related_name='restore_to_cluster', to='dbaas.Cluster'),
        ),
   ]
