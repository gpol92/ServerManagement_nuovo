from django.db import models

# Create your models here.

class Server(models.Model):
    ip = models.CharField(max_length=200)
    nome = models.CharField(max_length=100)
    domanda = models.TextField(default = 'ciao')
    risposta = models.TextField()
    tipoRisposta = models.TextField()

    def __str__(self):
        return self.ip +  " " + self.nome + " " + self.domanda + " " + self.risposta + " " + self.tipoRisposta

class Timer(models.Model):
    timer = models.CharField(max_length=10)

    def __str__(self):
        return self.timer

