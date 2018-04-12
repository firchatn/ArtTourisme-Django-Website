from django.conf.urls import url
from . import views
app_name = "art"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^errorlogin$', views.error, name='error'),
    url(r'^produits$', views.produits_view, name='produits_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^tunisie$', views.tunisie_view, name='tunisie_view'),
    url(r'^about$', views.about_view, name='about_view'),
    url(r'^contact$', views.contact_view, name='contact_view'),
    url(r'^event$', views.event_view, name='event_view'),
    url(r'^produit/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
]
