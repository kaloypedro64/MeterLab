from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    # path('', Calibration.as_view(), name='calibrated'),
    path('', views.calibration, name='calibrated'),

    path('edit/<int:id>', views.calibrate_edit, name='edit'),
    # for dropdown list
    path('consumer_list', views.consumer_list, name='consumer_list'),
    path('seal_list', views.seal_list, name='seal_list'),
    path('meters_list', views.meters_list, name='meters_list'),

    path('consumer_search', views.consumer_search, name='consumer_search'),
    path('consumer_save', views.consumer_save_assignedmeter, name='consumer_save'),
    path('calibration_update_save', views.calibration_update_save,
         name='calibration_update_save'),

    path('dt_meterseal_details/<int:id>', views.dt_meterseal_details,
         name='dt_meterseal_details'),

    path('print_calibration_history', views.print_calibration_history,
         name='print_calibration_history'),


]
