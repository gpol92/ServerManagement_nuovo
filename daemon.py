from cgitb import html
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
    listaPing = []
    timezone = pytz.timezone('Europe/Rome')
    servers = Server.objects.all()
    timer = Timer.objects.get(id = 1)
    while True:
        fileHtml = open('templates/test.html', 'w')
        fileStoricoPing = open('media/ReportServer.txt', 'w')
        fileServerKO = open('media/Server non funzionanti.txt', 'w')
        htmlContent = '''
<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <title>Storico e tempo reale</title>
    </head>
    <body>
        
        <form method="POST">
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <div class="collapse navbar-collapse">
                    <ul class="nav navbar-nav">
                        <li><a class="navbar-brand" href="{% url 'homepage' %} ">Home</a></li>
                        <li><a class="navbar-brand" href="{% url 'controlPanelPage' %}" class="subtitle" type="submit">Config</a></li>
                        <li><a href="{% url 'ping' %}" class="navbar-brand subtitle" type="submit">Check</a></li>
                        <li><a href="{% url 'storicoPing' %}" class="navbar-brand subititle" type="submit">Storico e tempo reale</a></li>
                    </ul>
                </div>
            </nav>
        </form>
        <p> Una volta avviato il ciclo di ping successivo la pagina diventa bianca; aggiornare la pagina quando il ciclo di ping è finito</p>
    </body>
</html>
'''
        fileHtml.write(htmlContent)
        for i in range(len(servers)):
            server = servers[i]
            ip = server.ip
            nome = server.nome
            tipoRisposta = server.tipoRisposta
            try: 
                response = requests.get(ip, timeout=(20, 20))
            except: 
                serverResponse = "Il server {} non funziona".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                fileServerKO.write(serverResponse)
                if len(listaPing) == 54:
                    listaPing.pop(0)
                listaPing.append(serverResponse)
                print("Il server {} non funziona".format(nome))
                send_mail(
                            'Report server',
                            'Il server {} non funziona.'.format(nome),
                            'g.polizia@athlos.biz',
                            #['info@athlos.biz'],
                            ['gpolizia5@gmail.com'],
                            fail_silently=False,
                )
            risposte = server.risposta.split("#")
            if tipoRisposta == 'stringa':
                if response.text.strip() in risposte:
                    print("Server {} Ok".format(nome))
                    serverResponse = "Il server {} è ok".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                    fileStoricoPing.write(serverResponse)
                    if len(listaPing) == 54:
                        listaPing.pop(0)
                    listaPing.append(serverResponse)
                else:
                    print("Il server {} non funziona".format(nome))
                    serverResponse = "Il server {} non funziona".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                    fileServerKO.write(serverResponse)
                    if len(listaPing) == 54:
                        listaPing.pop(0)
                    listaPing.append(serverResponse)
                    send_mail(
                            'Report server',
                            'Il server {} non funziona.'.format(nome),
                            'g.polizia@athlos.biz',
                            #['info@athlos.biz'],
                            ['gpolizia5@gmail.com'],
                            fail_silently=False,
                    )
            if tipoRisposta == 'dizionario':
                print(response.text)
                if response.text.strip() != "":
                    if response.json()['risposta'] in server.risposta:
                        print('Server {} Ok'.format(nome))
                        serverResponse = "Il server {} è ok".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                        fileStoricoPing.write(serverResponse)
                        if len(listaPing) == 54:
                            listaPing.pop(0)
                        listaPing.append(serverResponse)
                else: 
                    print('Il server {} non funziona'.format(nome))
                    serverResponse = "Il server {} non funziona".format(nome) + " " + datetime.now(tz=timezone).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                    fileServerKO.write(serverResponse)
                    if len(listaPing) == 54:
                            listaPing.pop(0)
                    listaPing.append(serverResponse)
                    send_mail(
                            'Report server',
                            'Il server {} non funziona.'.format(nome),
                            'g.polizia@athlos.biz',
                            #['info@athlos.biz'],
                            ['gpolizia5@gmail.com'],
                            fail_silently=False,
                    )
            fileStoricoPing.flush()
            fileServerKO.flush()
        fileStoricoPing.write("\n")
        fileStoricoPing.flush()
        htmlContent='''
<ul class="listaPing">
'''
        fileHtml.write(htmlContent)
        for esitoPing in listaPing:
                htmlContent = '''
                    <li>{}</li>
                '''.format(esitoPing)
                fileHtml.write(htmlContent)
        htmlContent = '''
<br>
</ul>
 <script>
        window.setTimeout(function () {
            location.reload()
        }, 5000);
</script>
        '''
        fileHtml.write(htmlContent)
        fileHtml.flush()
        fileHtml.close()
        fileStoricoPing.close()
        time.sleep(float(timer.timer)*60)

# righe di codice per eseguire la funzione main come script a se stante
if __name__ == '__main__':
    main()