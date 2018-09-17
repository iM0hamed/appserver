from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'appdistribution'

urlpatterns = [
    path('settings', views.settings, name='settings'),
    path('showapps', views.show_apps, name='showapps'),
    path('', views.index, name='index'),
    path('download', views.download_app, name='download'),
    path('upload', csrf_exempt(views.upload_apps), name='upload'),
    path('decode/<platform>/<product>/<file>', views.decode, name='decode')
]