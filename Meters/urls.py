from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    #     path('', views.meterList, name='meterList'),
    # meters
    path('', acquisitionList.as_view(), name='acqList'),
    path('acqadd/<int:id>', views.acquisition_add, name='acqadd'),
    path('acqsave', views.acquisition_save, name='acqsave'),
    path('acqselected/', views.acquisition_selected, name='acqselected'),
    path('delete/<int:id>/', views.acquisition_delete, name='acqdelete'),

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


#     path('get_supplier/<int:id>', views.get_supplier, name='get_supplier'),


    #     path('seriallist/<int:idmeters>/meter_test_report/<int:id>/',
    #          views.meter_test_report, name='meter_test_report'),

     #   brand
    path('brand', views.brand_ss, name='brandss'),
    path('brandsave', views.brand_save, name='brandsave'),
    path('branddelete', views.brand_delete, name='branddelete'),

    #   mTypes
    path('mtypes', views.mtypes_ss, name='mtypesss'),
    path('mtypessave', views.mtypes_save, name='mtypessave'),
    path('mtypesdelete', views.mtypes_delete, name='mtypesdelete'),

    path('meters', views.meter_ss, name='meterss'),
    path('meterssave', views.meter_save, name='meterssave'),
    path('metersdelete', views.meter_delete, name='metersdelete'),
]
