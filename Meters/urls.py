from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    #     path('', views.meterList, name='meterList'),
    # meters
    path('', MeterList.as_view(), name='rrviews'), 
    path('delete/<int:id>/', views.meters_delete, name='meters_delete'),
    path('add', views.meters_add, name='meters_add'),
    path('edit/<int:id>/', views.meters_edit, name='meters_edit'),

    # meter details
    path('meterdetails_ss/<int:id>/', views.meterdetails_ss, name='meterdetails_ss'),
    path('selected_meter/', views.selected_meter, name='selected_meter'),

    # calibrate
    path('meterdetails_ss/<int:idmeters>/calibrate_meter/<int:id>/',
         views.calibrate_meter, name='calibrate_meter'),

    path('delete_calibration/<int:id>/',
         views.delete_calibration, name='delete_calibration'),

    # path('save_selectedTable',views.save_selectedTable, name='save_selectedTable'),

#     path('seriallist/<int:idmeters>/edit/<int:id>/',
#          views.edit_meters, name='edit_meters'),


# #     path('meterlist/<int:id>', MeterList.as_view(), 'meterlist'),

#     path('multiple_calibration/<int:id>/',
#          views.multiple_calibration, name='multiple_calibration'),

#     path('seriallist/<int:idmeters>/meter_test_report/<int:id>/',
#          views.meter_test_report, name='meter_test_report'),


]
