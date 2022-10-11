import requests
import threading
import os 
import django
import time
from django.core.mail import send_mail
import sqlite3
from tkinter import *

print(django.__version__)
# try:
#     import controlPanel
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'controlPanel.settings')
#     django.setup()
# except ImportError:
#     print("Import Failed")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serverControl.settings')
django.setup()
from controlPanel.models import Server
from controlPanel.models import Timer

class threadLoop(threading.Thread):
    def __init__(self, timer, servers):
        self.timer = timer
        self.servers = servers
        threading.Thread.__init__(self)
    
    def run(self):
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
                        serverResponse = response.json()['risposta']
                        print(serverResponse)
                        if serverResponse == server.risposta:
                            response = 'Il server {} non funziona'.format(nome)
                            send_mail(
                                    'Report server',
                                    'Il server {} non funziona.'.format(nome),
                                    'g.polizia@athlos.biz',
                                    ['info@athlos.biz', 'gpolizia5@gmail.com'],
                                    fail_silently=False,
                            )
                    elif tipoRisposta == "stringa":
                        print(risposta)
                        inizio = response.text.find(risposta)
                        if inizio != -1:
                            sottostringa = response.text[inizio:inizio+len(risposta)]
                            if sottostringa == risposta:
                                print("Server ok")
                            else:
                                send_mail(
                                    'Report server',
                                    'Il server {} non funziona.'.format(nome),
                                    'g.polizia@athlos.biz',
                                    ['info@athlos.biz', 'gpolizia5@gmail.com'],
                                    fail_silently=False,
                                )
            time.sleep(float(timer.timer)*3600)


def modificaTimer():
    timer = entry1.get()
    print(timer)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    sql = '''
    UPDATE controlPanel_timer
    SET timer = ?
    '''

    valoreTimer = timer
    values = (float(valoreTimer),)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()



root = Tk()
root.geometry("700x700")

label1 = Label(root, text="Inserisci il timer in ore")
label1.place(relx=0.5, rely=0.18, anchor="center")
entry1 = Entry(root, width=50)
entry1.place(relx=0.5, rely=0.2, anchor="center")
button1 = Button(root, text="Imposta il timer", command=modificaTimer)
button1.place(relx=0.5, rely=0.29, anchor="center")
servers = Server.objects.all()
timer = Timer.objects.get(id = 1)
thread1 = threadLoop(timer, servers)
thread1.start()
root.mainloop()



