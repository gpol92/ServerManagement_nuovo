import requests
import os
import django
import time
from django.core.mail import send_mail
import pytz
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serverControl.settings')
django.setup()
from controlPanel.models import Server, Timer

def main():
    timezone = pytz.timezone('Europe/Rome')
    servers = Server.objects.all()
    timer = Timer.objects.get(id = 1)
    fileStoricoPing = open('media/ReportServer.txt', 'a')
    fileHtml = open('templates/test.html', 'a')
    htmlContent = '''
<html>
    <body>
'''
    fileHtml.write(htmlContent)
    while True:
        for i in range(len(servers)):
            server = servers[i]
            ip = server.ip
            nome = server.nome
            tipoRisposta = server.tipoRisposta
            response = requests.get(ip)
            risposte = server.risposta.split('#')
            for risposta in risposte:
                if tipoRisposta == 'dizionario':
                    if response.json()['risposta'] != server.risposta:
                        serverResponse = 'Il server {} non funziona'.format(nome)
                        fileStoricoPing.write(serverResponse + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                        send_mail(
                                'Report server',
                                'Il server {} non funziona.'.format(nome),
                                'g.polizia@athlos.biz',
                                ['info@athlos.biz'],
                                fail_silently=False,
                        )
                        break
                    else:
                        print("Server ok")
                        serverResponse = 'Il server {} è ok'.format(nome)
                        htmlContent = '''
            <p style="text-align: center;">{}</p>
                        '''.format(serverResponse + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                        fileStoricoPing.write(serverResponse + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                        fileHtml.write(htmlContent)
                elif tipoRisposta == "stringa":
                    print(risposta)
                    inizio = response.text.find(risposta)
                    if inizio != -1:
                        sottostringa = response.text[inizio:inizio+len(risposta)]
                        if sottostringa == risposta:
                            print("Server ok")
                            serverResponse = "Il server {} è ok".format(nome)
                            htmlContent = '''
            <p style="text-align: center;">{}</p>
                            '''.format(serverResponse + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                            fileStoricoPing.write(serverResponse + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                            fileHtml.write(htmlContent)
                        else:
                            send_mail(
                                'Report server',
                                'Il server {} non funziona.'.format(nome),
                                'g.polizia@athlos.biz',
                                ['info@athlos.biz'],
                                fail_silently=False,
                            )
        fileStoricoPing.write("\n")
        fileStoricoPing.flush()
        htmlContent = '''
            <br>
</body>
<html>
        '''
        fileHtml.write(htmlContent)
        fileHtml.flush()
        time.sleep(float(timer.timer)*60)

# righe di codice per eseguire la funzione main come script a se stante
if __name__ == '__main__':
    main()