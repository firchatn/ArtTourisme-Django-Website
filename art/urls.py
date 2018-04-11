from django.conf.urls import url
from . import views

app_name = "art"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^errorlogin$', views.error, name='error'),
]
