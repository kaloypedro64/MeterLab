from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', views.AssignedList, name='colist'),
    path('add/', views.assign, name='add'),
    path('selected_serialno/', views.selected_serialno, name='selected_serialno'),

]
