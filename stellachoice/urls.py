"""stellachoice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from baseapp import views as baseapp_views

admin.site.site_header = "Stella's Choice admin"
admin.site.site_title = "Stella's Choice Admin"
admin.site.index_title = "Stella's Choice administration"

urlpatterns = [
    path('', baseapp_views.home, name='home'),
    path('datavisual', baseapp_views.datavisual, name='datavisual'),
    path('about', baseapp_views.about, name='about'),
    path('alldogs', baseapp_views.alldogs, name='alldogs'),
    path('pdf_view', baseapp_views.pdf_view, name='pdf_view'),
    path('get_prediction', baseapp_views.ajax_adoption_speed, name='get_prediction'),
    path('admin/', admin.site.urls),
]
