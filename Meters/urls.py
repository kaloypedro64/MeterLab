from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    # path('', views.meterList, name='meterList'),
    # meters
    path('', meterList.as_view(), name='meterList'),
    path('details/', views.meters_detail, name='mdetails'),

    path('multiple/<int:id>', views.calibrate_multiple, name='multiple'),
    path('single/<int:id>', views.calibrate, name='calibrate'),

    # path('calibrations', views.calibration_history,
    #      name='calibrations'),

    path('consumer_list', views.consumer_list, name='consumer_list'),
    path('consumer_search', views.consumer_search, name='consumer_search'),
    path('consumer_save', views.consumer_save_assignedmeter, name='consumer_save'),

    path('consumers/<int:id>', views.load_assigned_consumers, name='consumers'),


#     path('edit/<int:id>/', views.meters_edit, name='meters_edit'),

#     # meter details
#     path('details/<int:id>/', views.meters_detail, name='metersdetail'),

#     path('details/<int:idmeters>/calibrate/<int:id>/',
#          views.calibrate, name='calibrate'),

#     # calibration
#     path('calibrate_delete/<int:id>/',
#          views.calibrate_delete, name='calibrate_delete'),

    # path('save_selectedTable',views.save_selectedTable, name='save_selectedTable'),

    #     path('seriallist/<int:idmeters>/edit/<int:id>/',
    #          views.edit_meters, name='edit_meters'),


#     path('get_supplier/<int:id>', views.get_supplier, name='get_supplier'),


    #     path('seriallist/<int:idmeters>/meter_test_report/<int:id>/',
    #          views.meter_test_report, name='meter_test_report'),


]
