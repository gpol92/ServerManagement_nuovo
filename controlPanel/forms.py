from django import forms
from django.forms import ModelForm
from .models import Server, Timer, User
from django.contrib.auth.forms import UserCreationForm

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

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('nome', 'cognome', 'email', 'password',)
        labels = {
            'nome': '',
            'cognome': '',
            'email': '',
            'password': '',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class:': 'form-control', 'placeholder': 'Inserisci il nome'}),
            'cognome': forms.TextInput(attrs={'class:': 'form-control', 'placeholder': 'Inserisci il cognome'}),
            'email': forms.TextInput(attrs={'class:': 'form-control', 'placeholder': 'Inserisci l\'email'}),
            'password': forms.TextInput(attrs={'class:': 'form-control', 'placeholder': 'Inserisci la password'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    nome = forms.CharField()
    cognome = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(), required=True)