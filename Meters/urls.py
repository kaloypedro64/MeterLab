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
    path('details/<int:id>/', views.meters_detail, name='metersdetail'),
    path('meter_selected/', views.meter_selected, name='meterselected'),

    path('details/<int:idmeters>/calibrate/<int:id>/',
         views.calibrate, name='calibrate'),

    # calibration
    path('calibrate_delete/<int:id>/',
         views.calibrate_delete, name='calibrate_delete'),
    path('details/<int:id>/calibrate_multiple/',
         views.calibrate_multiple, name='multiple'),

    # path('save_selectedTable',views.save_selectedTable, name='save_selectedTable'),

    #     path('seriallist/<int:idmeters>/edit/<int:id>/',
    #          views.edit_meters, name='edit_meters'),


    path('get_supplier/', views.get_supplier, name='get_supplier'),


    #     path('seriallist/<int:idmeters>/meter_test_report/<int:id>/',
    #          views.meter_test_report, name='meter_test_report'),


]
