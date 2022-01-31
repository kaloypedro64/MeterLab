"""MeterLab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import dashboard
from Meters.views import meter_test

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include("django.contrib.auth.urls")),
    path('', dashboard),
    path('home/', include('Users.urls')),
    path('acquisitions/', include('Acquisitions.urls')),
    path('meters/', include('Meters.urls')),
    path('calibration/', include('Calibration.urls')),
    path('metertest/', include('MeterTest.urls')),
    path('suppliers/', include('Suppliers.urls')),
    path('signatory/', include('Signatory.urls')),

    path('users/', include('Users.urls')),
    path('assign/', include('Assign.urls')),
    path('help/', include('help.urls')),
]
