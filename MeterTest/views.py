from decimal import Context
import types
from django.db.models import query
from django.db.models.query_utils import Q
from MeterLab.settings import AREA_CHOICES
from Users.models import userarea
from Users.forms import AreaForm
from django.contrib.auth.decorators import login_required
import math
import datetime
import time
import json
import json as json_util
from django.db import connection
from django.db.models.expressions import Window
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import *
from .models import *
from Meters.forms import *
from django.views.generic import *
from django.utils.dateparse import parse_datetime

from django.core.cache import cache
from django.urls import reverse
from django.utils.cache import get_cache_key

from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

datetoday = datetime.date.today()
datenow = datetime.datetime.now()

header = 'Meter Test'

html_metertest_history = "meter_test/meter_test_history.html"
html_metertest = "meter_test/meter_test.html"
html_metertestreport = 'reports/meter_test_report.html'

# @login_required(login_url='/')
class meter_test(ListView):
    model = metertest
    html = html_metertest_history

    def get_queryset(self):
        return self.model.objects.select_related('consumers').filter(serialno__icontains=self.request.GET.get('filter'),).values('id', 'gen_average', 'serialno', 'consumersid__consumer', 'testdate').order_by(self.request.GET.get('order_by'))

    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            list_data = []
            for index, item in enumerate(self.get_queryset().filter(acquisitionid__area=transaction_area.area)[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), 'application/json')
        else:
            return render(request, self.html, {'header': 'Meters', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})

def meter_test_details(request):
    if request.is_ajax():
        id = str(request.GET.get('id'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        query = metertest.objects.select_related('consumers').filter(serialno__icontains=filter,).values(
            'id', 'gen_average', 'serialno', 'consumersid__consumer', 'testdate').order_by(order_by)

        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), 'application/json')

@csrf_exempt
def meter_test_new(request, serialno):
    form = metertestForm(request.POST)
    if request.method == "POST":
        print('form.is_valid()', form.is_valid())
        if form.is_valid():
            form.save()
        print(form.errors)
        return HttpResponseRedirect('..')
    else:
        context = {'form': form, 'datetoday': datetoday, 'serialno': serialno}
        return render(request, html_metertest, context)


def search_for_meter(request):
    if request.is_ajax():
        serial = request.GET.get('serial')
        cursor = connection.cursor()
        cursor.execute("select accountnumber, name, address, serial, billmonth, totalbill, meterbrand from zaneco.master where serial <> '' and serial like '" +
                       str(serial) + "'")
        data = cursor.fetchall()
        try:
            name = data[0][1]
            address = data[0][2]
            serial = data[0][3]
            brand = data[0][6]
        except:
            data = {'msg':'not found!'}
            return HttpResponse(json.dumps(data, default=default), 'application/json')

        # get brand
        try:
            _brand = brands.objects.get(brand__contains=brand)
            brandid = _brand.id
        except brands.DoesNotExist:
            cursor.execute("""INSERT INTO zanecometerpy.brands(brand)
                    SELECT * FROM(SELECT '{0}') as tmp
                    WHERE NOT EXISTS(SELECT brand FROM zanecometerpy.brands WHERE brand LIKE '{0}')
                            LIMIT 1""".format(brand))
            brandid = cursor.lastrowid

        cursor.execute("insert into zanecometerpy.consumers (consumer, address) select * from (select '" + name +
                       "', '" + address + "') as tmp where not exists (select consumer from zanecometerpy.consumers where consumer like '" + name + "');")
        query = "select id, consumer, address, '{2}' serial, '{3}' brand, '{4}' brandid from zanecometerpy.consumers where consumer like '{0}' and address like '{1}' ".format(
            name, address, serial, brand, brandid)
        cursor.execute(query)


        data = cursor.fetchall()

        # print('context', data)
    return HttpResponse(json.dumps(data, default=default), 'application/json')

# print
def load_test_print(request, id):
    #         return self.model.objects.select_related('brand', 'mtype', 'acquisition').values('id', 'acquisitionid', 'acquisitionid__transactiondate', 'brandid__brand',
    #                                                                                          'mtypeid__metertype', 'mtypeid', 'ampheres', 'serialnos', 'units', 'acquisitionid__area').order_by(self.request.GET.get('order_by'))
    # queryset = metertest.objects.select_related('consumers', 'brands').get(id=id)
    queryset = metertest.objects.select_related('brandid', 'consumersid').values('id', 'testdate', 'serialno', 'gen_average', 'fullload_average', 'lightload_average', 'fl1',
                                                                                 'fl2', 'fl3', 'll1', 'll2', 'll3', 'reading', 'type', 'volts', 'phase', 'kh', 'ta', 'remarks', 'active', 'isdamage', 'userid', 'brandid__brand', 'consumersid__consumer', 'consumersid__address').get(pk=id)
    # print('queryset', queryset)
    # serials = meterdetails.objects.get(pk=queryset.meterdetailsid.id)
    context = {'form': queryset,'idmeters': id}
    return render(request, html_metertestreport, context)

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
