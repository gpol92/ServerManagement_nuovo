# Generated by Django 3.2.6 on 2022-10-04 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlPanel', '0010_auto_20221004_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='risposta',
            field=models.TextField(default='ciao benvenuto sono qui per chiarire i tuoi dubbi a proposito del superbonus come ottenerlo le verifiche preliminari i destinatari i salti di classe energetica gli interventi possibili i problemi di agibilità pre e post operam'),
        ),
    ]
