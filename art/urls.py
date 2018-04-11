from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', 'commerce.views.index', name='root'),
    url(r'^sign-in/(?P<goto>\w+:\w+)/$', 'commerce.views.sign_in', name='sign_in_goto'),
    url(r'^sign-in/$', 'commerce.views.sign_in', name='sign_in'),
    url(r'^sign-out/$', 'commerce.views.sign_out', name='sign_out'),
    url(r'^product/(?P<product_id>\d+)/$', 'commerce.views.display_product', name='display_product'),
    url(r'^category/(?P<category_id>\d+)$', 'commerce.views.display_category', name='display_category'),
    url(r'^add-to-cart/(?P<product_id>\d+)/(?P<qty>\d+)/$', 'commerce.views.add_to_cart', name='add_to_cart'),
    url(r'^clear-cart/$', 'commerce.views.clear_cart', name='clear_cart'),
    url(r'^cart/$', 'commerce.views.display_cart', name='display_cart'),
    url(r'^shipping/$', 'commerce.views.shipping', name='shipping'),
    url(r'^add-address/$', 'commerce.views.add_address', name='add_address'),
    url(r'^checkout/$', 'commerce.views.checkout', name='checkout'),
    url(r'^confirmation/$', 'commerce.views.confirmation', name='confirmation'),
    url(r'^account/$', 'commerce.views.account', name='account'),
    url(r'^orders/$', 'commerce.views.orders', name='orders'),
    url(r'^addresses/$', 'commerce.views.addresses', name='addresses'),
]
