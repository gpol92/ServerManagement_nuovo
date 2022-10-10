from django.db import models

# Create your models here.

class Server(models.Model):
    ip = models.CharField(max_length=200)
    nome = models.CharField(max_length=100)
    domanda = models.TextField(default = 'ciao')
    risposta = models.TextField(default = '''
    ciao benvenuto sono disponibile per darti informazioni riguardo al superbonus come ottenerlo le verifiche preliminari i destinatari i salti di classe energetica gli interventi possibili i problemi di agibilità pre e post operam#ciao benvenuto sono qui per chiarire i tuoi dubbi a proposito del superbonus come ottenerlo le verifiche preliminari i destinatari i salti di classe energetica gli interventi possibili i problemi di agibilità pre e post operam#ciao benvenuto il mio compito è di rispondere alle tue domande a proposito del superbonus come ottenerlo le verifiche preliminari i destinatari i salti di classe energetica gli interventi possibili i problemi di agibilità pre e post operam''')
    tipoRisposta = models.TextField(default="stringa")

    def __str__(self):
        return self.ip +  " " + self.nome + " " + self.domanda + " " + self.risposta + " " + self.tipoRisposta

class Timer(models.Model):
    timer = models.CharField(max_length=10)
    
    def __str__(self):
        return self.timer