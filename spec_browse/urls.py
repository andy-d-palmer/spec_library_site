__author__ = 'palmer'

from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^detail/mol(?P<pk>[0-9]+)/$', views.mol_detail, name='mol_detail'),
    url(r'^sf/(?P<pk>[0-9]+)/$', views.sf_detail, name='sf_detail'),
]
