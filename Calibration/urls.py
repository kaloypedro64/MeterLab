from django.urls import path, include
# from . import views
from .views import *

urlpatterns = [
    path('', CalibrationList.as_view(), name='calibrationviews'),
]