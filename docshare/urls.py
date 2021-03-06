"""docshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from docshareapp import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^create_Folder/', views.create_folder, name='createFolder'),
    url(r'^listdir/', views.list_directory, name='listDir'),
    url(r'^download/', views.download, name='downloadFile'),
    url(r'^upload/', views.upload, name='uploadFile'),
    url(r'^search/',views.search, name='searchFor'),
    url(r'^autocomplete',views.autocomplete, name='autoComplete'),
    url(r'^delete/',views.delete, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)