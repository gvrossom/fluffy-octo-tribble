# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'datahub'
urlpatterns = [
    url(r'^user/(?P<username>[-\w]+)/$', views.document_user,
        name='document_user'),
    url(r'^files/upload/$', views.document_create,
        name='document_create'),
    url(r'^files/edit/(?P<pk>\d+)/$', views.document_edit,
        name='document_edit'),
    url(r'^files/$', views.document_list, name='document_list'),
	# ex: /documents/5/
    url(r'^create/$', views.folder_create,
        name='folder_create'),
    url(r'^edit/(?P<pk>\d+)/$', views.folder_edit,
        name='folder_edit'),
    url(r'^(?P<folder_id>[0-9]+)/$', views.folder_detail, name='folder_detail'),
	# ex: /datahub/
    url(r'^$', views.folder_list, name='folder_list'),
]
