from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Server, Timer
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import ServerForm, TimerForm
import requests
from time import sleep
from django.core.mail import send_mail
from datetime import datetime
import threading
import os
import json
import pytz
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormView, DeleteView
import shutil

# Create your views here.

#Thread per gestire l'invio della mail in caso di server non funzionante
class EmailThread(threading.Thread):

    def __init__(self, nome):
        self.nome = nome
        threading.Thread.__init__(self)

    def run(self):
        
        print("Un server non funziona. Invio mail di segnalazione")
        send_mail(
            'Report server',
            'Il server {} non funziona.'.format(self.nome),
            'g.polizia@athlos.biz',
            #['info@athlos.biz'],
            ['gpolizia5@gmail.com'],
            fail_silently=False,
        )

class HomepageView(TemplateView):
    template_name = 'homepage.html'
# def homepage(request):
#     return render(request, 'homepage.html')

# view per renderizzare nella pagina il contenuto del database dei server
class ConfigView(TemplateView):
    template_name = 'config.html'

    def get_context_data(self, **kwargs):
        servers = Server.objects.all()
        try:
            timer = Timer.objects.get(pk=1)
            print(timer)
        except Timer.DoesNotExist:
            # Handle the case where the Timer object is not found
            print("Timer with ID 1 not found.")
            timer = None

        timerAttuale = timer.timer if timer else None
        context = super().get_context_data(**kwargs)
        context['servers'] = servers
        context['timer'] = timerAttuale
        return context

# def config(request):
#     servers = Server.objects.all()
#     timer = Timer.objects.get(pk=1)
#     timerAttuale = timer.timer
#     context = {"servers": servers, 'timer': timerAttuale}
#     return render(request, 'config.html', context)

# view per l'aggiunta dei server al db
class AddServerView(FormView):
    template_name = 'addServer.html'
    form_class = ServerForm
    success_url = 'addServer'
    def form_valid(self, form):
        form = ServerForm(self.request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('addServer')
            
# def addServer(request):
#     submitted = False
#     if request.method == 'POST':
#         form = ServerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/addServer?submitted=True')
#     else:
#         form = ServerForm
#         if 'submitted' in request.GET:
#             submitted = True
#     return render(request, 'addServer.html', {'form': form, 'submitted': submitted})

#view che implementa l'inserimento e aggiornamento del timer
class InserisciTimerView(FormView):
    template_name = 'insertTimer.html'
    form_class = TimerForm
    success_url = 'insertTimer'
    def post(self, request):
        form = TimerForm
        currentTimer = Timer.objects.get(pk=1)
        newTimer = request.POST['timer']
        currentTimer.timer = newTimer
        currentTimer.save()
        return render(request, self.template_name, {'form': form})
    
# def inserisciTimer(request):
#     submitted = False
#     currentTimer = Timer.objects.get(pk=1)
#     if request.method == 'POST':
#         newTimer = request.POST['timer']
#         currentTimer.timer = newTimer
#         currentTimer.save()
#         return HttpResponseRedirect('/insertTimer?submitted=True')
#     else: 
#         form = TimerForm
#         if 'submitted' in request.GET:
#             submitted = True
#     return render(request, 'insertTimer.html', {'form': form, 'submitted': submitted, 'timer': currentTimer.timer})


# view per cancellare server dal database
class DeleteServerView(View):
    def get(self, server_id):
        server = Server.objects.get(pk=server_id)
        server.delete()
        return redirect('config')
# def deleteServer(request, server_id):
#     server = Server.objects.get(pk=server_id)
#     server.delete()
#     return redirect('config')

# view che effettua ciclicamente il ping di tutti i server presenti nel database. La view utilizza un timer salvato in una tabella del database.
# La view salva in un file di testo un messaggio sullo stato dei server.
class PingView(TemplateView):
    def post(self, request):
        timezone = pytz.timezone('Europe/Rome')
        servers = Server.objects.all() 
        responses = []
        timer = Timer.objects.get(id=1)
        timer = timer.timer
        while True:
            f = open()
def ping(request):
    timezone = pytz.timezone('Europe/Rome')
    servers = Server.objects.all() 
    responses = []
    timer = Timer.objects.get(id=1)
    timer = timer.timer
    while True:
        f = open('media/ReportServer.txt', 'w')
        f2 = open('media/Server non funzionanti.txt', 'w')
        if request.method == 'POST':
            for i in range(len(servers)):
                server = servers[i]
                ip = server.ip
                nome = server.nome
                tipoRisposta = server.tipoRisposta
                response = requests.get(ip)
                risposte = server.risposta.split("#")
                if tipoRisposta == 'stringa':
                    if response.text.strip() in risposte:
                        print("Server {} Ok".format(nome))
                        serverResponse = "Il server {} è ok".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"        
                        f.write(serverResponse)
                        responses.append(serverResponse)      
                    else:
                        print("Il server {} non funziona".format(nome))
                        serverResponse = "Il server {} non funziona".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                        f2.write(serverResponse)
                        emailThread1 = EmailThread(nome)
                        emailThread1.start() 
                        responses.append(serverResponse)
                if tipoRisposta == 'dizionario':
                    print(response.text)
                    if response.text.strip() != "":
                        if response.json()['risposta'] in server.risposta:
                            print('Server {} Ok'.format(nome))
                            serverResponse = "Il server {} è ok".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                            f.write(serverResponse)
                            responses.append(serverResponse)
                    else: 
                        print('Il server {} non funziona'.format(nome))
                        serverResponse = "Il server {} non funziona".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n" 
                        f2.write(serverResponse)
                        emailThread1 = EmailThread(nome)
                        emailThread1.start() 
                        responses.append(serverResponse) 
            f.write("\n")
        f.flush()
        f2.flush()
        f.close()
        f2.close()
        sleepThread1 = sleepThread(timer)
        sleepThread1.start()
        return render(request, 'ping.html', {'risposte': responses})


class sleepThread(threading.Thread):
    def __init__(self, timer):
        self.timer = timer
        threading.Thread.__init__(self)
    def run(self):
        sleep(float(self.timer)*60)
#view che implementa il download dello storico dei ping

def storicoPing(request):
    # source = 'media/ReportServer.txt'
    # destination = 'templates/ReportServer.txt'
    # dest = shutil.copyfile(source, destination)
    # contents = open('media/ReportServer.txt', 'r')
    # with open('templates/storico.html', 'w') as storico:
    #     for lines in contents.readlines():
    #         storico.write("<pre>" + lines + "</pre> <br>\n")
    # return render(request, 'storico.html')
    return render(request, 'test.html')

def download(request):
    if os.path.exists('media/ReportServer.txt'):
        file = open('media/ReportServer.txt')
        response = HttpResponse(file.read(), content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'storico_ping.txt'
        return response
    return render(request, 'ping.html')

# view per il download del file che registra i server non funzionanti
def err_download(request):
    if os.path.exists('media/Server non funzionanti.txt'):
        file = open('media/Server non funzionanti.txt')
        response = HttpResponse(file.read(), content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'Server non funzionanti.txt'
        return response
    return render(request, 'ping.html')

def remove_file(request):
    if os.path.exists('media/Server non funzionanti.txt'):
        os.remove('media/Server non funzionanti.txt')
        os.remove('media/ReportServer.txt')
        
    else:
        return render(request, 'ping.html')
    return render(request, 'ping.html')

# class LoopPing(threading.Thread):

#     def __init__(self,request):
#         self.request = request
#         threading.Thread.__init__(self)

#     def run(self):
#         while True:
#             print("Inizio esecuzione thread")
#             ping(self.request)
#             sleep(0.005*3600)           


# def configuraTimer(request, timerValue):
#     print(request.method)
#     if request.method == 'GET':
#         print(request.GET.get('timer'))
#         print(timerValue)
#     # filename = 'timer.json'
#     # to_json = {
#     #     'timerValue': timerValue
#     # }  
#     # response = HttpResponse(json.dumps(to_json), content_type='application/json')
#     # response['Content-Disposition'] = 'attachment; filename{0}'.format(filename)
#     return render(request, 'configuraTimer.html')

# def configuraTimer(request):
#     timerValue = request.GET.get('timer')
#     filename = 'timer.json'
#     to_json = {
#         'timerValue': timerValue
#     }  
#     response = HttpResponse(json.dumps(to_json), content_type='application/json')
#     response['Content-Disposition'] = 'attachment; filename{0}'.format(filename)
#     return response


# def pingWithTimer(request):
#     for _ in range(2):
#         ping()
#         sleep(0.016*3600)
#     return render(request, 'ping.html')

# def pingWithTimer(request):
#     loopPing1 = LoopPing(request)
#     loopPing1.start()
#     return render(request, 'ping.html')


# class PingThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
    
#     def run(self):
#         f = open('media/Report Server.txt', 'a')
#         responses = []
#         servers = Server.objects.all()
        
#         while True:
#             for i in range(len(servers)):
#                 server = servers[i]
#                 ip = server.ip
#                 nome = server.nome
#                 response = requests.get(ip)
#                 if response.text == server.risposta:
#                     print("Server ok")
#                     response = "Il server {} è OK".format(nome)
#                     f.write(response + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
#                     response = (response, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
#                     # emailThread1 = EmailThread(nome)
#                     # emailThread1.start()
#                     # loopPing1 = LoopPing(request)
#                     # loopPing1.start()
#                     responses.append(response)
#                 else:
#                     response = "Il server {} è disattivo".format(nome)
#                     f.write(response + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
#                     response = (response, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
#                     # emailThread1 = EmailThread(nome)
#                     # emailThread1.start()
#                     responses.append(response)
#                 f.write("\n")


# def startPing(request):
#     servers = Server.objects.all()
#     context = {"servers": servers}
#     print(context)
#     if request.method == 'POST':
#         indirizzoIP = request.POST.get('indirizzoIP')
#         timer = request.POST.get('timer')
#         indirizzoIP = "http://" + indirizzoIP
#         response = requests.get(indirizzoIP)
#         if response != "":
#             response = "Server OK"
#             # send_mail(
#             #     'Report server',
#             #     '{}'.format(response),
#             #     'rosMarino46@yandex.com',
#             #     ['gpolizia5@gmail.com'],
#             #     fail_silently=False,
#             #     )   
#             print(response)
#             # sleep(float(timer)*3600)    
#     return render(request, 'controlPanelPage.html', context)
