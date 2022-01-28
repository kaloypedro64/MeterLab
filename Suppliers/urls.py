from django.urls import path, include


from . import views
from .views import *

urlpatterns = [
    path('', SuppliersList.as_view(), name='suppliers'),
    path('getsupplierdetails', views.getSupplierDetails, name='getsupplierdetails'),
    path('savesupplier', views.saveSupplier, name='savesupplier'),
    path('editsupplier', views.editSupplier, name='editsupplier'),
    path('delsupplier', views.delSupplier, name='delsupplier'),
]

