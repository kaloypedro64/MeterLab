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

    path('meter-test-details/', views.meter_test_details, name='testdetails'),
    path('meter-test/', views.meter_test, name='test'),
    path('meter-test-new/<str:serialno>', views.meter_test_new, name='new'),

    # path('calibrations', views.calibration_history,
    #      name='calibrations'),

    path('serials', views.serial_list, name='serials'),
    path('search_for_meter', views.search_for_meter, name='search_for_meter'),










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
