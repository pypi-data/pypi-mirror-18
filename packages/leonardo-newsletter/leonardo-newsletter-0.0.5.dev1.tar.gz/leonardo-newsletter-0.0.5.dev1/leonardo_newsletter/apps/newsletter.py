"""Default urls for the emencia.django.newsletter"""
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^mailing/',
                           include('emencia.django.newsletter.urls.mailing_list')),
                       url(r'^', include('emencia.django.newsletter.urls.newsletter')),
                       )
