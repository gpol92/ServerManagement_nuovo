# Generated by Django 3.2.6 on 2022-10-12 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlPanel', '0018_alter_server_tiporisposta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='risposta',
            field=models.TextField(),
        ),
    ]
