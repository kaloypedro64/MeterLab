from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    # path('', views.meterList, name='meterList'),
    # meters
    path('', meter_test.as_view(), name='metertest'),
    path('meter-test-new/<str:serialno>', views.meter_test_new, name='new'),
    path('search_for_meter', views.search_for_meter, name='search_for_meter'),
    path('print_test/<int:id>', views.load_test_print, name='print_test'),
    path('prepare_summary', views.prepare_summary, name='prepare_summary'),
    # path('preview_summary',views.preview_summary, name='preview_summary'),


]
