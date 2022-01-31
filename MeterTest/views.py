from cgitb import lookup
from decimal import Context
from multiprocessing import context
import types
from django.db.models import query
from django.db.models.query_utils import Q
from MeterLab.settings import AREA_CHOICES
from Signatory.models import signatory
from Users.models import userarea
from Users.forms import AreaForm
from django.contrib.auth.decorators import login_required
import math
import datetime
import time
import json
import json as json_util
from django.db import connection, connections
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
# findings = {' gen_average__lte = 98', ' gen_average__gte 99', ''}
header = 'Meter Test'

html_metertest_history = "meter_test/meter_test_history.html"
html_metertest = "meter_test/meter_test.html"
html_metertestreport = 'reports/print_meter_test_report.html'
html_metertestreport_summary = 'reports/print_meter_test_report_summary.html'

# @login_required(login_url='/')
class meter_test(ListView):
    model = metertest
    html = html_metertest_history

    def get_queryset(self):
        return self.model.objects.select_related('consumers').values('id', 'gen_average', 'serialno', 'consumersid__consumer', 'testdate').order_by(self.request.GET.get('order_by'))

    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            status = request.GET.get('status')
            datefrom = request.GET.get('datefrom')
            dateto = request.GET.get('dateto')
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            filter = request.GET.get('filter')
            lookups = Q(serialno__icontains=filter) | Q(
                consumersid__consumer__icontains=filter)
            if int(status) == 1:
                lookupb = Q(gen_average__lte = 98)
            elif int(status) == 2:
                lookupb = Q(gen_average__gte = 99)
            else:
                lookupb = Q(gen_average__gte=0)
            if datefrom:
                lookupdate = Q(testdate__range = [datefrom, dateto])
            else:
                lookupdate = Q(testdate__range=[datenow.replace(day=1), datenow.replace(day=31)])
            list_data = []
            for index, item in enumerate(self.get_queryset().filter(lookups, lookupb, lookupdate)[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), 'application/json')
        else:
            return render(request, self.html, {'header': 'Meters', 'datetoday': datetoday, 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})

# def meter_test_details(request):
#     if request.is_ajax():
#         status = request.GET.get('status')
#         datefrom = request.GET.get('datefrom')
#         dateto = request.GET.get('dateto')
#         id = str(request.GET.get('id'))
#         start = int(request.GET.get('start'))
#         limit = int(request.GET.get('limit'))
#         filter = request.GET.get('filter')
#         order_by = request.GET.get('order_by')
#         lookups = Q(serialno__icontains=filter) | Q(consumersid__consumer__icontains=filter)
#         query = metertest.objects.select_related('consumers').filter(lookups).values(
#             'id', 'gen_average', 'serialno', 'consumersid__consumer', 'testdate').order_by(order_by)

#         list_data = []
#         for index, item in enumerate(query[start:start+limit], start):
#             list_data.append(item)
#         data = {
#             'length': query.count(),
#             'objects': list_data,
#         }
#         return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), 'application/json')

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
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.is_ajax():
        serial = request.GET.get('serial')
        zancursor = connections['zaneco'].cursor()
        if (transaction_area.area == 1):
            zancursor = connections['zaneco_pas'].cursor()
        elif (transaction_area.area == 2):
            zancursor = connections['zaneco_sas'].cursor()
        elif (transaction_area.area == 3):
            zancursor = connections['zaneco_las'].cursor()
        zancursor.execute("select accountnumber, name, address, serial, billmonth, totalbill, meterbrand from zaneco.master where serial <> '' and serial like '" +
                        str(serial) + "'")

        data = zancursor.fetchall()
        try:
            name = data[0][1]
            address = data[0][2]
            serial = data[0][3]
            brand = data[0][6]
        except:
            data = {'msg':'not found!'}
            return HttpResponse(json.dumps(data, default=default), 'application/json')
        # get brand
        cursor = connection.cursor()
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
    transaction_area = userarea.objects.get(userid=request.user.id)
    signs = signatory.objects.filter(area=transaction_area.area).first()
    queryset = metertest.objects.select_related('brandid', 'consumersid').values('id', 'testdate', 'serialno', 'gen_average', 'fullload_average', 'lightload_average', 'fl1',
                                                                                 'fl2', 'fl3', 'll1', 'll2', 'll3', 'reading', 'type', 'volts', 'phase', 'kh', 'ta', 'remarks', 'active', 'isdamage', 'userid', 'brandid__brand', 'consumersid__consumer', 'consumersid__address').get(pk=id)
    context = { 'form': queryset, 'idmeters': id, 'signs':signs }
    return render(request, html_metertestreport, context)


def prepare_summary(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    status = request.GET.get('id')
    date_from = request.GET.get('range')
    d_range = date_from.split('|')
    if int(status) == 1:
        lookupb = Q(gen_average__lte = 98)
    elif int(status) == 2:
        lookupb = Q(gen_average__gte = 99)
    else:
        lookupb = Q(gen_average__gte=0)
    if d_range[0]:
        lookupdate = Q(testdate__range=[d_range[0], d_range[1]])
    else:
        lookupdate = Q(testdate__range=[datenow.replace(day=1), datenow.replace(day=31)])
    signs = signatory.objects.filter(area=transaction_area.area).first()
    query = metertest.objects.select_related('consumers').filter(lookupb, lookupdate).values(
    'id', 'consumersid__consumer', 'serialno', 'reading',  'gen_average')
    context = {'form': query, 'signs': signs, 'date_from': d_range[0], 'date_to': d_range[1]}
    return render(request, html_metertestreport_summary, context)

# def preview_summary(request):
#     return render(request, html_metertestreport_summary, {})

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
