from django.urls import path

from .views import HomepageView, LoginView, RegistrationView, ConfigView, DeleteServerView, AddServerView, ping, storicoPing, download, InserisciTimerView, err_download, remove_file
urlpatterns = [
    #view homepage
    path('', HomepageView.as_view(), name='homepage'),
    # login
    path('login', LoginView.as_view(), name="login"),
    path('register', RegistrationView.as_view(), name="register"),
    # visualizzazione dei server e i pulsanti per l'aggiunta e la rimozione
    path('config', ConfigView.as_view(), name="config"),
    # rimozione di un server
    path('<pk>/deleteServer', DeleteServerView.as_view(), name='delete-server'),
    # aggiunta di un server
    path('addServer', AddServerView.as_view(), name='add-server'),
    #ping in ore
    path('ping', ping, name='ping'),
    # visualizzazione storico ping da file .txt
    path('storicoPing', storicoPing, name='storicoPing'),
    #download del file con lo storico dei ping
    path('download_txt', download, name='download_txt'),
    # inserimento del timer
    path('insertTimer', InserisciTimerView.as_view(), name='insertTimer'),
    # download del file con i server non funzionanti
    path('err_download', err_download, name='err_download'),
    # rimozione del file con i server non funzionanti
    path('cancella_storico', remove_file, name='cancella_storico')
]