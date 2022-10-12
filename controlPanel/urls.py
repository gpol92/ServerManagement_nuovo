from django.urls import path

from .views import homepage, controlPanelPage, deleteServer, addServer, ping, download, inserisciTimer, err_download, remove_file
urlpatterns = [
    #view homepage
    path('', homepage, name='homepage'),
    # visualizzazione dei server e i pulsanti per l'aggiunta e la rimozione
    path('controlPanel', controlPanelPage, name="controlPanelPage"),
    # rimozione di un server
    path('deleteServer/<server_id>', deleteServer, name='delete-server'),
    # aggiunta di un server
    path('addServer', addServer, name='add-server'),
    #ping in ore
    path('ping', ping, name='ping'),
    #download del file con lo storico dei ping
    path('download_txt', download, name='download_txt'),
    # inserimento del timer
    path('insertTimer', inserisciTimer, name='insertTimer'),
    # download del file con i server non funzionanti
    path('err_download', err_download, name='err_download'),
    # rimozione del file con i server non funzionanti
    path('cancella_storico', remove_file, name='cancella_storico')
]