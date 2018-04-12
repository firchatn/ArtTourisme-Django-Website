from django.conf.urls import url
from . import views
app_name = "art"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^errorlogin$', views.error, name='error'),
    url(r'^produits$', views.produits_view, name='produits_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
]
