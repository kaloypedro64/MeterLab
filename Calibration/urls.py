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
    path('update_seal', views.calibration_update_save, name='update_seal'),

    path('meterseal/<int:id>', views.load_meterseal, name='meterseal'),

    path('print_test/<int:id>', views.load_test_print, name='print_test'),
]
