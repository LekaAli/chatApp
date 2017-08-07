from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^start_server/',views.startServer,name='startserver'),
    # url(r'^stop_server/',views.stopServer,name='stopserver'),

]
