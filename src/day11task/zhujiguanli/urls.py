#_*_coding:utf-8_*_
"""day11task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/',register),
    url(r'^login/$', login),
    url(r'^index/$', index),
    url(r'^user/$', user),
    url(r'^usertype/$', usertype),
    url(r'^group/$', group),
    url(r'^groupupdate/(?P<groupid>\d+)/$',groupupdate),
    url(r'^host/$', host),
    url(r'^hostupdate/(?P<hostid>\d+)/$', hostupdate),
    url(r'^adduser/',adduser),
    url(r'^showuser/$',showuser,{'groupid':'all'}),
    url(r'^showuser/(?P<groupid>\d+)/$',showuser),
    url(r'^deleteuser/(?P<groupid>\d+)/',deleteuser),
    url(r'^deleteuser/$',deleteuser,{'groupid':''}),
    url(r'^deleteuser/(?P<groupid>\d+)/$',deleteuser),
    url(r'^$',login),
    url(r'^logout',logout),
]
