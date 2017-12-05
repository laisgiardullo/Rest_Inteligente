"""video_inteligente_gui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
import os
import settings

urlpatterns = [

    url(r'^realtime/', 'realtime.views.index', name='perguntas'),
    url(r'^home_admin/', 'realtime.views.home_admin', name='home_admin'),
    url(r'^historico_admin/', 'realtime.views.historico_admin', name='historico_admin'),
    url(r'^admin/', admin.site.urls),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        
    
            {'document_root': os.path.join(os.getcwd(),'static') }),
]
