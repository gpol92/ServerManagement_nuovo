# Generated by Django 3.2.6 on 2022-10-03 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controlPanel', '0007_alter_server_timer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='timer',
        ),
    ]
