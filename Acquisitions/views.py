import types
from django.db.models import query
from django.db.models.query_utils import Q
from MeterLab.settings import AREA_CHOICES
from Users.models import userarea
from Users.forms import AreaForm
import math
import datetime
import time
import json
import json as json_util
from django.db import connection
from django.db.models.expressions import Window
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from Meters.models import *
from Meters.forms import *
from django.views.generic import CreateView, FormView, RedirectView, ListView
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

datetoday = datetime.date.today()

header = 'Dashboard'
html_aAdd = 'acquisitions/acquisition_add.html'
html_msAdd = 'acquisitions/acquisition_add_mseal.html'
login_url = 'login'

# html_meterlist = 'meters/meter_list.html'
# html_mAdd = "meters/meter_request_add.html"
# html_mEdit = "meters/meter_request_edit.html"
# html_meterdetails_data = 'meters/meterdetails_data.html'
# html_meters_data = 'meters/meters_data.html'
# html_metertestreport = 'meters/meter_test_report.html'

html_calibration = 'calibration/calibrate.html'

class acquisitionList(ListView):
    model = acquisition
    html = 'acquisitions/acquisitions.html'

    def get_queryset(self):
        return self.model.objects.select_related('suppliers').filter(supplierid__suppliername__icontains=self.request.GET.get('filter')).values('id', 'transactiondate', 'rrnumber', 'supplierid__suppliername', 'supplierid__address', 'area').order_by(self.request.GET.get('order_by'))

    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            acqtype = int(request.GET.get('acqtype'))
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            list_data = []
            for index, item in enumerate(self.get_queryset().filter(area=transaction_area.area, acqtype=acqtype)[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            return HttpResponse(json.dumps(data, default=default), 'application/json')
        else:
            mform = acquisitionForm(request.POST)
            mSupplier = suppliers.objects.order_by('suppliername').distinct()
            return render(request, self.html, {'header': 'Meters', 'form': mform, 'mSupplier': mSupplier, 'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'datetoday': datetoday, 'area': transaction_area.area})


# def acquisition_selected(request):
#     if request.is_ajax():
#         id = request.GET.get('id')
#         queryset = acquisition.objects.filter(pk=id).order_by('id')
#         context = {'trans': queryset, 'id': id}
#         return render(request, html_meters_data, context)


@login_required(login_url=login_url)
def acquisition_save(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.method == "GET":
        date = request.GET.get('transactiondate')
        rrno = request.GET.get('rrno')
        supplierid = request.GET.get('supplierid')
        acqtype = request.GET.get('acqtype')
        now = datetime.datetime.utcnow()
        cursor = connection.cursor()
        cursor.execute('insert into zanecometerpy.acquisition (transactiondate, rrnumber, area, userid, supplierid, acqtype, created_at, updated_at) values ("' + date + '","' + rrno + '","' +
                       transaction_area.area + '","' + str(request.user.id) + '","' + str(supplierid) + '", "' + str(acqtype) + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '", "' + now.strftime('%Y-%m-%d %H:%M:%S') + '")')
        cursor.fetchall()
        id = cursor.lastrowid
        if True:
            data = {"id":id, "msg": 'saved', 'acqtype':acqtype}
        else:
            data = {"msg": 'Not saved'}
        print('data',data)
        return HttpResponse(json.dumps(data, default=default), 'application/json')

@login_required(login_url=login_url)
def acquisition_add(request, id):
    transaction_area = userarea.objects.get(userid=request.user.id)
    acq = acquisition.objects.select_related('supplierid').values(
        'id', 'transactiondate', 'rrnumber', 'supplierid__suppliername', 'supplierid__address').get(pk=id)
    mBrand = brands.objects.order_by('brand').distinct()
    mTypes = mtype.objects.order_by('metertype').distinct()
    mAmp = meters.objects.values('ampheres').order_by('ampheres').distinct()
    mSupplier = suppliers.objects.order_by('suppliername').distinct()
    context = {'header': 'Meter Acquisition', 'datetoday': datetoday, 'acq':acq, 'area': transaction_area.area,
                'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'mBrand': mBrand, 'mTypes': mTypes, 'mAmp': mAmp, 'mSupplier': mSupplier}
    return render(request, html_aAdd, context)

def acquisition_edit(request, id):
    if request.is_ajax():
        id = request.GET.get('id')
        acqinfo = acquisition.objects.get(pk=id)
        # acqinfo.delete()

        if True:
            data = {"form": acqinfo }
        else:
            data = {"msg": 'Not found'}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')


def acquisition_delete(request, id):
    if request.is_ajax():
        id = request.GET.get('id')
        acqinfo = acquisition.objects.get(pk=id)
        acqinfo.delete()

        # meterinfo_details = meterdetails.objects.get(idmeters=id)
        # meterinfo_details.delete()

        if True:
            data = {"msg": 'deleted'}
        else:
            data = {"msg": 'Not deleted'}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')


def meter_ss(request):
    if request.is_ajax():
        id = str(request.GET.get('id'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        query = meters.objects.select_related('brand', 'mtype').filter(acquisitionid=id).values('id', 'acquisitionid', 'brandid', 'brandid__brand',
                                                                                            'mtypeid__metertype', 'mtypeid', 'ampheres', 'serialnos', 'units').order_by(order_by)
        # print('query', query.query)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def meter_save(request):
    if request.is_ajax():
        acquisitionid = str(request.GET.get('acquisitionid'))
        brandid = str(request.GET.get('brandid'))
        mtypeid = str(request.GET.get('mtypeid'))
        ampheres = str(request.GET.get('ampheres'))
        serialnos = str(request.GET.get('serialnos'))
        units = str(request.GET.get('units'))


        cursor = connection.cursor()
        cursor.execute('insert into zanecometerpy.meters (acquisitionid, brandid, mtypeid, ampheres, serialnos, units) values ("' + acquisitionid + '","' + brandid + '","' + mtypeid + '","' + ampheres + '","' + serialnos + '","' + units + '")')
        cursor.fetchall()
        meterid = cursor.lastrowid

        serials = serialnos.split('-')

        num1 = int(serials[0])
        zerofill = len(serials[0])

        for index in range(1, int(units) + 1):
            num = num1
            num = str(num).zfill(zerofill)
            cursor.execute('insert into zanecometerpy.meterdetails (meterid,serialno,accuracy,wms_status,status,active) ' +
                           'values ("' + str(meterid) + '","' + num + '",0,0,0,0)')
            cursor.fetchall()
            num1 += 1

        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def meter_delete(request):
    if request.is_ajax():
        id = request.GET.get('id')
        meterinfo = meters.objects.get(pk=id)
        meterinfo.delete()
        if True:
            data = {"msg": 'deleted'}
        else:
            data = {"msg": 'Not deleted'}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')


#  start brand
def brand_ss(request):
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        order_by = request.GET.get('order_by')
        query = brands.objects.values('id', 'brand').order_by(order_by)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def brand_save(request):
    if request.is_ajax():
        brand = str(request.GET.get('brand'))
        cursor = connection.cursor()
        cursor.execute(
            'insert into zanecometerpy.brands (brand) values ("' + str(brand) + '")')
        cursor.fetchall()
        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def brand_delete(request):
    if request.is_ajax():
        id = int(request.GET.get('id'))
        cursor = connection.cursor()
        cursor.execute(
            'delete from zanecometerpy.brands where id = "' + str(id) + '"')
        cursor.fetchall()
        if True:
            data = {"msg": 'deleted'}
        else:
            data = {"msg": 'Not deleted'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')
#  end brand

# start meter type


def mtypes_ss(request):
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        order_by = request.GET.get('order_by')
        query = mtype.objects.values('id', 'metertype').order_by(order_by)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def mtypes_save(request):
    if request.is_ajax():
        metertype = str(request.GET.get('metertype'))
        cursor = connection.cursor()
        cursor.execute(
            'insert into zanecometerpy.metertype (metertype) values ("' + str(metertype) + '")')
        cursor.fetchall()
        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def mtypes_delete(request):
    if request.is_ajax():
        id = int(request.GET.get('id'))
        cursor = connection.cursor()
        cursor.execute(
            'delete from zanecometerpy.metertype where id = "' + str(id) + '"')
        cursor.fetchall()
        if True:
            data = {"msg": 'deleted'}
        else:
            data = {"msg": 'Not deleted'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')
# end meter type


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

