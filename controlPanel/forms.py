from django import forms
from django.forms import ModelForm
from .models import Server, Timer

class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields=('ip', 'nome', 'domanda', 'risposta', 'tipoRisposta')

        labels = {
            'ip': '',
            'nome': '',
            'domanda': '',
            'risposta': '',
            'tipoRisposta': ''
        }

        widgets = {
            'ip': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Server Ip'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Server'}),
            'domanda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domanda'}),
            'risposta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Risposta (Inserire la lista di risposte separate da cancelletto)'}),
            'tipoRisposta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TipoRisposta (inserire stringa o dizionario)'}),
        }

class TimerForm(ModelForm):
    class Meta:
        model = Timer
        fields = ('timer',)

        labels = {
            'timer': '',
        }

        widgets = {
            'timer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Timer in minuti'}),
        }

