import sqlite3
from tkinter import *
import requests


conn = sqlite3.connect('db.sqlite3')
#creazione cursore
cursor = conn.cursor()
# sql = '''DELETE FROM controlPanel_server WHERE id=15'''
# cursor.execute(sql)
# conn.commit()
# conn.close()

def startPing(indirizzoIP):
    ipAddress = str(indirizzoIP.get())
    try: 
        response = requests.get("http://"+ipAddress)
        strVarResponse = StringVar()
        if response.text != "":
            response = "Server OK"
            strVarResponse.set(response)
            responseLabel = Label(root, textvariable=strVarResponse)
            responseLabel.pack()
        else: 
            response = "Server KO"
            strVarResponse.set(response)
            responseLabel = Label(root, textvariable=strVarResponse)
            responseLabel.pack()

    except ConnectionError:
        responseLabel = Label(root, text="Connection Error")
        responseLabel.pack()

def ping():
    label5 = Label(root, text="Inserisci l'indirizzo ip del server")
    label5.pack()
    indirizzoIP = StringVar()
    entry5 = Entry(root, width=50, textvariable=indirizzoIP)
    entry5.pack()
    button2 = Button(root, text="startPing", command=lambda:startPing(indirizzoIP))
    button2.pack()

def insertInDb(ipServer, nomeServer, cursor):
    sql = '''INSERT INTO controlPanel_server (ip, nome) VALUES (?, ?)'''
    values = (str(ipServer.get()), str(nomeServer.get()))
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def deleteFromDb(nomeServer, cursor):
    sql = '''DELETE FROM controlPanel_server WHERE nome=?'''
    nomeServerTupla = (str(nomeServer.get()),)
    cursor.execute(sql, nomeServerTupla)
    conn.commit()
    conn.close()

def insert():
    label1 = Label(root, text="Inserisci l'indirizzo ip del server")
    label1.pack()
    ipServer = StringVar()
    entry1 = Entry(root, width=50, textvariable=ipServer)
    entry1.pack()
    label2 = Label(root, text="Inserisci il nome del server")
    label2.pack()
    nomeServer = StringVar()
    entry2= Entry(root, width=50, textvariable=nomeServer)
    entry2.pack()
    button1 = Button(root, text="Submit", command=lambda:insertInDb(ipServer, nomeServer, cursor))
    button1.pack()

def delete():
    label4 = Label(root, text="Inserisci il nome del server")
    label4.pack()
    nomeServer = StringVar()
    entry4= Entry(root, width=50, textvariable=nomeServer)
    entry4.pack()
    button2 = Button(root, text="Submit", command=lambda:deleteFromDb(nomeServer, cursor))
    button2.pack()



root = Tk()
root.title('Menù')
root.geometry("1000x1000")
scelte = Menu(root)
root.config(menu=scelte)
server_menu = Menu(scelte)
scelte.add_cascade(label="Aggiungi server, elimina server o effettua il ping", menu=server_menu)
server_menu.add_command(label="Inserisci server nel database", command=insert)
server_menu.add_separator()
server_menu.add_command(label="Elimina server dal database", command=delete)
server_menu.add_separator()
server_menu.add_command(label="Effettua il ping del server", command=ping)
server_menu.add_separator()
server_menu.add_command(label="Chiudi", command=root.quit)
root.mainloop()





    


