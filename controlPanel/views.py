from django.shortcuts import render, redirect
from .models import Server, Timer
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import ServerForm, TimerForm
import requests
from time import sleep
from django.core.mail import send_mail
from datetime import datetime
import threading
from wsgiref.util import FileWrapper
import os
import json
from django.views.generic import TemplateView
import shutil

# Create your views here.


# porzione di codice per gestire il timer nel ciclo while nella view ping
continue_looping = True
def stopper():
    global continue_looping
    continue_looping = False

class EmailThread(threading.Thread):

    def __init__(self, nome):
        self.nome = nome
        threading.Thread.__init__(self)

    def run(self):
        
        print("ThreadingExecution started")
        send_mail(
            'Report server',
            'Il server {} non funziona.'.format(self.nome),
            'g.polizia@athlos.biz',
            ['gpolizia5@gmail.com'],
            fail_silently=False,
        )

def homepage(request):
    return render(request, 'homepage.html')

# view per renderizzare nella pagina il contenuto del database dei server
def controlPanelPage(request):
    servers = Server.objects.all()
    timer = Timer.objects.get(pk=1)
    timerAttuale = timer.timer
    context = {"servers": servers, 'timer': timerAttuale}
    return render(request, 'controlPanelPage.html', context)

# view per l'aggiunta dei server al db
def addServer(request):
    submitted = False
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addServer?submitted=True')
    else:
        form = ServerForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'addServer.html', {'form': form, 'submitted': submitted})

#view che implementa l'inserimento e aggiornamento del timer
def inserisciTimer(request):
    submitted = False
    currentTimer = Timer.objects.get(pk=1)
    if request.method == 'POST':
        newTimer = request.POST['timer']
        currentTimer.timer = newTimer
        currentTimer.save()
        return HttpResponseRedirect('/insertTimer?submitted=True')
    else: 
        form = TimerForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'insertTimer.html', {'form': form, 'submitted': submitted, 'timer': currentTimer.timer})


# view per cancellare server dal database

def deleteServer(request, server_id):
    server = Server.objects.get(pk=server_id)
    server.delete()
    return redirect('controlPanelPage')

# view che effettua ciclicamente il ping di tutti i server presenti nel database. La view utilizza un timer salvato in una tabella del database.
# La view salva in un file di testo un messaggio sullo stato dei server.

def ping(request):
    servers = Server.objects.all() 
    responses = []
    timer = Timer.objects.get(id=1)
    timer = timer.timer
    f = open('media/ReportServer.txt', 'a')
    f2 = open('media/Server non funzionanti.txt', 'a')
    while True:
        if request.method == 'POST':
            for i in range(len(servers)):
                server = servers[i]
                ip = server.ip
                nome = server.nome
                tipoRisposta = server.tipoRisposta
                response = requests.get(ip)
                print(server.risposta)
                # print(len(server.risposta))
                # print(response.text)
                risposte = server.risposta.split('#')
                for risposta in risposte:
                    if tipoRisposta == 'dizionario':
                        # rispostaFrase = response.text
                        # print(rispostaFrase)
                        rispostaJson = response.json()
                        print(rispostaJson)
                        # print(id(rispostaJson))
                        # print(id(server.risposta))
                        # print([ord(C) for C in rispostaJson])
                        # print([ord(C) for C in server.risposta])
                        # parole = rispostaJson.split(" ")
                        # print(parole)
                        if rispostaJson['risposta'] == server.risposta:
                            print("Server ok")
                            serverResponse = "Il server {} è OK".format(nome)
                            f.write(serverResponse + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                            serverResponse = (serverResponse, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                            responses.append(serverResponse)
                        else:
                            serverResponse = "Il server {} è disattivo".format(nome)
                            f2.write(serverResponse + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n\n")
                            serverResponse = (serverResponse, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                            emailThread1 = EmailThread(nome)
                            emailThread1.start()
                            responses.append(serverResponse)
                            break
                    elif tipoRisposta == 'stringa':
                        inizio = response.text.find(risposta)
                        print(inizio)
                        if inizio != -1:
                            sottostringa = response.text[inizio:inizio+len(risposta)]
                            print(sottostringa)
                            if sottostringa == risposta:
                                print("Server ok")
                                serverResponse = "Il server {} è OK".format(nome)
                                f.write(serverResponse + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                                serverResponse = (serverResponse, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                                responses.append(serverResponse)
                            else:
                                serverResponse = "Il server {} è disattivo".format(nome)
                                f2.write(serverResponse + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                                serverResponse = (serverResponse, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                                emailThread1 = EmailThread(nome)
                                emailThread1.start()
                                responses.append(serverResponse)
                continue
            f.write("\n") 
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
