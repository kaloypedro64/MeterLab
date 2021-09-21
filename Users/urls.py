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
from django.urls import path
from django.urls.conf import include
from MeterLab .views import dashboard as home

from .views import *

urlpatterns = [
    # path('', LoginView.as_view(), name='login'),
    path('', login, name='login'),
    path('home', home, name='home'),
    path('regs', register, name='register'),
    path('logout', logout_view, name='logout'),
    path('list', UserList.as_view(), name='list'),
    path('edit/<int:id>/', edit_users, name='edit'),


    # path('admin/', admin.site.urls),
]