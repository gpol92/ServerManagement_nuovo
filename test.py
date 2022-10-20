import requests

risposta = 'ciao benvenuto, il mio compito è di aiutarti a fissare un appuntamento#ciao benvenuto, sono a tua disposizione per assisterti nel fissare un appuntamento#ciao benvenuto, la mia funzione è di guidarti nella procedura di prenotazione di un appuntamento'
ip = 'http://192.168.1.194/aika2/aika2_vm_proxy.php?apikey=ang&question=ciao&trace=0'
response = requests.get(ip)
print(response.text)
risposte = risposta.split('#')
response = response.text.strip()
response = response.lstrip()
response = response.rstrip()
print(risposte)
for ris in risposte:
        print(repr(ris))
        print(repr(response))
        print("\n")