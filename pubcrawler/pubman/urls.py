from django.conf.urls import url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^authors/(?P<letter>[a-zA-Z])/$', views.authors_index, name='authors'),
    url(r'^publications/$', views.pub_index, name='publications'),
    url(r'^authors/(?P<author_id>[0-9]+)/$', views.author_detail, name='author_detail'),
    url(r'^publications/(?P<pub_id>[0-9]+)/$', views.publication_detail, name='publication_detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^author_create/$', views.author_create, name='author_create'),
]
