from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$', views.index),
    url(r'^product/(?P<product_id>[0-9]\d*)/$', views.productPage),
    url(r'^addToCart/(?P<product_id>[0-9]\d*)/$', views.addToCart)
]