from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^request_connection',views.requestConnection,name='requestconnection'),
    url(r'^send/',views.sendMessage,name='sendchat'),
]
