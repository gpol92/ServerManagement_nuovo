# Generated by Django 3.2.6 on 2022-10-12 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlPanel', '0016_alter_server_risposta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='risposta',
            field=models.TextField(default='\n    ciao benvenuto sono disponibile per darti informazioni riguardo al superbonus come ottenerlo le verifiche preliminari i destinatari i salti di classe energetica gli interventi possibili i problemi di agibilità pre e post operam#ciao benvenuto sono qui per chiarire i tuoi dubbi a proposito del superbonus come ottenerlo le verifiche preliminari i destinatari i salti di classe energetica gli interventi possibili i problemi di agibilità pre e post operam#ciao benvenuto il mio compito è di rispondere alle tue domande a proposito del superbonus come ottenerlo le verifiche preliminari i destinatari i salti di classe energetica gli interventi possibili i problemi di agibilità pre e post operam'),
        ),
        migrations.AlterField(
            model_name='server',
            name='tipoRisposta',
            field=models.TextField(default='stringa'),
        ),
    ]
