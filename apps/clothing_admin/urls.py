from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^processLogin/$', views.processLogin),
    url(r'^orders/$', views.orders),
    url(r'^login/$', views.login),
    url(r'^logout/$',views.logout),
    url(r'^products/$', views.products),
    url(r'^addProduct/$', views.addProduct),
    url(r'^processNew/$', views.processNew),
    url(r'^test/$', views.test),
    url(r'^processTest/$', views.processTest),
    url(r'^delete/(?P<product_id>[0-9]\d*)/$', views.deleteProduct),
    url(r'^edit/(?P<product_id>[0-9]\d*)/$', views.editProduct),
    url(r'^processEdit/(?P<product_id>[0-9]\d*)/$', views.processEdit),
    url(r'^orderInfo/(?P<order_id>[0-9]\d*)/$', views.orderInfo),
    url(r'^changeStatus/(?P<order_id>[0-9]\d*)/$', views.changeStatusAPI),
    url(r'^batchInfo/$', views.batchInfo),
    url(r'^batchInfo/viewLocation/(?P<location_id>[0-9]\d*)/$', views.viewLocation),
    url(r'^batchInfo/viewBatch/(?P<batch_id>[0-9]\d*)/$', views.viewBatch),
    url(r'^batchConfirm/(?P<batch_id>[0-9]\d*)/$', views.batchConfirm),
    url(r'^finalizeBatch/(?P<batch_id>[0-9]\d*)/$', views.finalizeBatch),
    url(r'^searchAPI/$', views.searchAPI),
]