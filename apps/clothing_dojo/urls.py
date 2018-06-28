from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$', views.index),
    url(r'^login_page/$', views.loginPage),
    url(r'^processLogin/$', views.processLogin),
    url(r'^logout/$', views.logout),
    url(r'^product/(?P<product_id>[0-9]\d*)/$', views.productPage),
    url(r'^addToCart/(?P<product_id>[0-9]\d*)/$', views.addToCart),
    url(r'^cart/$', views.cart),
    url(r'^removeCart/(?P<cartitem_id>[0-9]\d*)/$', views.removeFromCart),
    url(r'^checkout/$', views.checkout),
    url(r'^processCheckout/$', views.processCheckout)
]