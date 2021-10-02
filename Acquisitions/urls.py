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
