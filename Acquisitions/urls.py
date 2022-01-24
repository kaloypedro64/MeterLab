from django.urls import path, include
from . import views
from .views import *

urlpatterns = [

    path('', acquisitionList.as_view(), name='acqList'),
    path('acqadd/<int:id>', views.acquisition_add, name='acqadd'),
    path('acqsave', views.acquisition_save, name='acqsave'),
    # path('acqselected/', views.acquisition_selected, name='acqselected'),
    path('edit/<int:id>/', views.acquisition_edit, name='acqedit'),
    path('delete/<int:id>/', views.acquisition_delete, name='acqdelete'),

    # dropdown
    path('rrnumbers', views.rrnumber_list, name='rrnumbers'),
    path('suppliers', views.supplier_list, name='suppliers'),
    path('selected_rrnumber', views.selected_rrnumber, name='selected_rrnumber'),
    path('selected_supplier', views.selected_supplier, name='selected_supplier'),

    # meter brands
    path('brand', views.brand_ss, name='brandss'),
    path('brandsave', views.brand_save, name='brandsave'),
    path('branddelete', views.brand_delete, name='branddelete'),

    #   mTypes
    path('mtypes', views.mtypes_ss, name='mtypesss'),
    path('mtypessave', views.mtypes_save, name='mtypessave'),
    path('mtypesdelete', views.mtypes_delete, name='mtypesdelete'),

    # meters
    path('meters', views.meter_ss, name='meterss'),
    path('meterssave', views.meter_save, name='meterssave'),
    path('meter_edit', views.meter_edit, name='meter_edit'),
    path('metersdelete', views.meter_delete, name='metersdelete'),

    # seals
    path('acqadds/<int:id>', views.acquisition_adds, name='acqadds'),
    path('seals', views.seal_ss, name='sealss'),
    path('sealssave', views.seal_save, name='sealssave'),
    path('sealsdelete', views.seal_delete, name='sealsdelete'),

    # accept, cancel acquisition

    path('acquisition_response', views.acquisition_response,
         name='acquisition_response'),

    path('get_meter_details', views.get_meter_details, name='get_meter_details'),

]

