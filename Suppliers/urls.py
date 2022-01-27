from django.urls import path, include


from . import views
from .views import *

urlpatterns = [
    path('', SuppliersList.as_view(), name='suppliers'),
    # path('', views.Signatories, name='signatory'),
]

