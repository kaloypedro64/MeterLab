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
from .forms import *
from django.views.generic import *
from django.utils.dateparse import parse_datetime

from django.core.cache import cache
from django.urls import reverse
from django.utils.cache import get_cache_key

from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

datetoday = datetime.date.today()

header = 'Dashboard'
# html_mAdd = "meters/acquisition_add_meter.html"
# html_msAdd = "meters/acquisition_add_seal.html"

html_meterlist = 'meters/meter_list.html'
html_mAdd = "meters/meter_request_add.html"
html_mEdit = "meters/meter_request_edit.html"
html_meterdetails_data = 'meters/meterdetails_data.html'
html_meters_data = 'meters/meters_data.html'

html_metertest_history = "meter-test/meter_test_history.html"
html_metertest = "meter-test/meter_test.html"
html_metertestreport = 'meter-test/meter_test_report.html'

html_calibration = 'calibration/calibrate.html'
html_calibration_multi = 'calibration/calibration_multiple.html'


# @login_required(login_url='/')
# class meterList(ListView):
#     model = meters
#     html = 'meters/meters.html'

#     def get_queryset(self):
#         return self.model.objects.select_related('brand', 'mtype', 'acquisition').values('id', 'acquisitionid', 'acquisitionid__transactiondate', 'brandid__brand',
#                                                                                          'mtypeid__metertype', 'mtypeid', 'ampheres', 'serialnos', 'units', 'acquisitionid__area').order_by(self.request.GET.get('order_by'))
#     def get(self, request, *args, **kwargs):
#         transaction_area = userarea.objects.get(userid=request.user.id)
#         if request.is_ajax():
#             start = int(request.GET.get('start'))
#             limit = int(request.GET.get('limit'))
#             list_data = []
#             for index, item in enumerate(self.get_queryset().filter(acquisitionid__area=transaction_area.area)[start:start+limit], start):
#                 list_data.append(item)
#             data = {
#                 'length': self.get_queryset().count(),
#                 'objects': list_data,
#             }
#             return HttpResponse(json.dumps(data, default=default), 'application/json')
#         else:
#             return render(request, self.html, {'header': 'Meters', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})



# def meters_add(request):
#     transaction_area = userarea.objects.get(userid=request.user.id)
#     if request.method == "POST":
#         form = meterForm(request.POST)
#         if form.is_valid():
#             rec = form.save()
#             rec.save()

#             # save meter serials for manual meter entry
#             cursor = connection.cursor()
#             idmeters = rec.id
#             units = request.POST['units']
#             now = datetime.datetime.utcnow()
#             serials = request.POST['serialnos'].split('-')

#             num1 = int(serials[0])
#             zerofill = len(serials[0])

#             for index in range(1, int(units) + 1):
#                 num = num1
#                 num = str(num).zfill(zerofill)
#                 cursor.execute('insert into zanecometerpy.meterdetails (idmeters, serialno, wms_status, userid, created_at, updated_at) ' +
#                                'values ("' + str(idmeters) + '","' + num + '","0","' + str(request.user.id) + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '")')
#                 cursor.fetchall()
#                 num1 += 1
#         return redirect("/meters")
#     else:
#         form = meterForm(request.POST)
#         mBrand = meters.objects.values('brand').order_by('brand').distinct()
#         mType = meters.objects.values(
#             'metertype').order_by('metertype').distinct()
#         mAmp = meters.objects.values(
#             'ampheres').order_by('ampheres').distinct()
#         mSupplier = get_supplier()
#         context = {'form': form, 'header': 'Add Meter', 'datetoday': datetoday, 'area': transaction_area.area,
#                    'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'mBrand': mBrand, 'mType': mType, 'mAmp': mAmp, 'mSupplier': mSupplier}
#         return render(request, html_mAdd, context)


# def meters_edit(request, id):
#     transaction_area = userarea.objects.get(userid=request.user.id)
#     if request.method == "POST":
#         queryset = meters(pk=id)
#         form = meterForm(request.POST, instance=queryset)
#         print(form.is_valid)
#         if form.is_valid():
#             created = request.POST.get('created_at')
#             rec = form.save(commit=False)
#             rec.created_at = datetoday
#             rec.save()
#             # form.save()
#         return redirect("/meters")
#     else:
#         queryset = meters.objects.get(pk=id)
#         mBrand = meters.objects.values('brand').order_by('brand').distinct()
#         mType = meters.objects.values(
#             'metertype').order_by('metertype').distinct()
#         mAmp = meters.objects.values(
#             'ampheres').order_by('ampheres').distinct()
#         mSupplier = get_supplier()
#         context = {'form': queryset, 'header': 'Edit Meter',
#                    'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'mBrand': mBrand, 'mType': mType, 'mAmp': mAmp, 'mSupplier': mSupplier}
#         return render(request, html_mEdit, context)


def meters_detail(request):
    if request.is_ajax():
        id = str(request.GET.get('id'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        query = meterdetails.objects.select_related('meters').filter(meterid=id,
                                                                     serialno__icontains=filter,).values('id', 'serialno',
                                                                                                         'accuracy', 'wms_status', 'status', 'active').order_by(order_by)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def meter_test_details(request):
    if request.is_ajax():
        id = str(request.GET.get('id'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        # SELECT id, '', gen_average, serialno, consumers FROM zanecometerpy.metertest
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

def meter_test(request):
    return render(request, html_metertest_history, {})


@csrf_exempt
def meter_test_new(request, serialno):
    form = metertestForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('..')
    else:
        context = {'form': form, 'datetoday': datetoday, 'serialno': serialno}
        return render(request, html_metertest, context)

def calibrate(request, id):
    if request.method == "POST":
        form = metertestForm(request.POST)
        if form.is_valid():
            form.save()
            # meterdetailsid = request.POST['meterdetailsid']
            average = request.POST['gen_average']
            cursor = connection.cursor()
            cursor.execute('update zanecometerpy.meterdetails set wms_status=1, status = if("' + str(
                average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(id) + '"')
            cursor.fetchall()
            return redirect("../")
        else:
            data = {"err_msg": form.errors}
            return JsonResponse(data)
    else:
        serials = meterdetails.objects.get(id=id)
        form = metertestForm(request.POST)
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'meterdetailsid': id}
        return render(request, html_calibration, context)


def calibrate_multiple(request, id):
    serials = meterdetails.objects.filter(
        meterid=id).filter(wms_status__exact=0)
    form = metertestForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            meterid = request.POST['idmeterdetails']
            average = request.POST['gen_average']
            cursor = connection.cursor()
            cursor.execute(
                'update zanecometerpy.meterdetails set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(meterid) + '"')
            cursor.fetchall()
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': id, 'save': 'save'}
        return render(request, html_calibration_multi, context)
    else:
        # serials = meterserials.objects.filter(idmeters=id).filter(wms_status__exact=0)
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': id}
        return render(request, html_calibration_multi, context)

# start load data to select2 option - serverside dropdown

def consumer_list(request):
    if request.is_ajax():
        search = request.GET.get('searchTerm')
        cursor = connection.cursor()
        query = "SELECT idnewapply id, concat(name, ' - ', ornumber) name, address, ordate, ornumber FROM zanecoisd.newapply "
        if search:
            query += "where name like '%" + search + "%'"
        cursor.execute(query)
        consumers = cursor.fetchall()
        datas = []
        list_data = []
        for index, item in enumerate(consumers):
            list_data.append(item)
        for s in range(len(list_data)):
            data = {
                'id': list_data[s][0],
                'text': list_data[s][1],
            }
            datas.append(data)
    return HttpResponse(json.dumps(datas, default=default), 'application/json')

def serial_list(request):
    if request.is_ajax():
        search = request.GET.get('searchTerm')
        cursor = connection.cursor()
        query = "select code id, serial from zaneco.master "
        if search:
            query += "where TRIM(COALESCE(serial, '')) <> '' and (serial like '" + \
                search + "%')"
        cursor.execute(query)
        consumers = cursor.fetchall()
        datas = []
        list_data = []
        for index, item in enumerate(consumers):
            list_data.append(item)
        for s in range(len(list_data)):
            data = {
                'id': list_data[s][0],
                'text': list_data[s][1],
            }
            datas.append(data)
    return HttpResponse(json.dumps(datas, default=default), 'application/json')

def search_for_meter(request):
    if request.is_ajax():
        serial = request.GET.get('serial')
        cursor = connection.cursor()
        cursor.execute("select accountnumber, name, address, serial, billmonth, totalbill, meterbrand from zaneco.master where serial <> '' and serial like '" +
                       str(serial) + "'")
        data = cursor.fetchall()
        name = data[0][1]
        address = data[0][2]
        serial = data[0][3]
        brand = data[0][6]
        cursor.execute("insert into zanecometerpy.consumers (consumer, address) select * from (select '" + name +
                       "', '" + address + "') as tmp where not exists (select consumer from zanecometerpy.consumers where consumer like '" + name + "');")
        # cursor.fetchall()
        # consumerid = cursor.lastrowid

        # context = {'consumerid':consumerid}
        query = "select id, consumer, address, '{2}' serial, '{3}' brand from zanecometerpy.consumers where consumer like '{0}' and address like '{1}' ".format(name, address, serial, brand)
        cursor.execute(query)
        data = cursor.fetchall()

        # print('context', data)
    return HttpResponse(json.dumps(data, default=default), 'application/json')

def seal_list(request):
    if request.is_ajax():
        search = request.GET.get('searchTerm')
        query = sealdetails.objects.filter(serialno__icontains=search, active__icontains=0).values('id', 'sealid', 'meterdetailsid',
                                                                                                   'serialno', 'techcrew', 'status', 'active').order_by('serialno')
        list_data = []
        datas = []
        list_data = []
        for index, item in enumerate(query):
            list_data.append(item)
        for s in range(len(list_data)):
            data = {
                'id': list_data[s]['id'],
                'text': list_data[s]['serialno'],
            }
            datas.append(data)
    return HttpResponse(json.dumps(datas, default=default), 'application/json')
# end load data to select2 option - serverside dropdown


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
