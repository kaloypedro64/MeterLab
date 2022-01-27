from functools import partialmethod
import types
from django.db.models import Sum
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
html_mAdd = 'acquisitions/acquisition_add_meter.html'
html_msAdd = 'acquisitions/acquisition_add_meter_seal.html'
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
        return self.model.objects.select_related('suppliers').exclude(status=4).filter(supplierid__suppliername__icontains=self.request.GET.get('filter'), ).values('id', 'transactiondate', 'rrnumber', 'supplierid__suppliername', 'supplierid__address', 'area', 'status').order_by('-transactiondate')

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


# get rrnumbers from warehouse - dropdown
def rrnumber_list(request):
    if request.is_ajax():
        search = request.GET.get('searchTerm')
        cursor = connection.cursor()
        query = "SELECT idreceipts id, rrnumber from zanecoinvphp.tbl_receipts "
        if search:
            query += "where rrnumber like '%" + search + "%' "
        query += "order by idreceipts desc"
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

def selected_rrnumber(request):
    if request.is_ajax():
        id = request.GET.get('id')
        cursor = connection.cursor()
        query = "SELECT idreceipts id, rrnumber, r.idsupplier, suppliers, address " + \
                "    from zanecoinvphp.tbl_receipts r " + \
                "    left join zanecoinvphp.tbl_supplier s on s.suppliername = r.suppliers " + \
                "    where idreceipts = '"+ id +"' "
        cursor.execute(query)
        rrnumber = cursor.fetchall()
        if True:
            data = {"form": rrnumber}
        else:
            data = {"msg": 'Not found'}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')

def supplier_list(request):
    if request.is_ajax():
        search = request.GET.get('searchTerm')
        cursor = connection.cursor()
        query = "SELECT id, suppliername, address from suppliers "
        if search:
            query += "where suppliername like '%" + search + "%' "
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

def selected_supplier(request):
    if request.is_ajax():
        id = request.GET.get('id')
        cursor = connection.cursor()
        query = "SELECT idsupplier id, suppliername, address from zanecoinvphp.tbl_supplier where idsupplier = '" + id + "' "
        cursor.execute(query)
        suppliers = cursor.fetchall()
        if True:
            data = {"form": suppliers}
        else:
            data = {"msg": 'Not found'}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')

@login_required(login_url=login_url)
def acquisition_save(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.method == "GET":
        date = request.GET.get('transactiondate')
        rrno = request.GET.get('rrno')
        supplierid = request.GET.get('supplierid')
        suppliername = request.GET.get('suppliername')
        address = request.GET.get('address')
        acqtype = request.GET.get('acqtype')
        now = datetime.datetime.utcnow()
        cursor = connection.cursor()
        cursor.execute('select suppliername from zanecometerpy.suppliers where suppliername like "' + str(suppliername) + '"')
        locate_supplier = cursor.fetchone()
        if locate_supplier == None:
            cursor.execute('insert into zanecometerpy.suppliers (suppliername, address) values ("'+ str(suppliername) +'", "'+ str(address) +'")')
            supplierid = cursor.lastrowid
        else:
            cursor.execute('select id from zanecometerpy.suppliers where suppliername like "'+ str(suppliername) +'" limit 1')
            locate_supplier = cursor.fetchall()
            supplierid = locate_supplier[0][0]
        # print(supplierid, supplierid)
        cursor.execute('insert into zanecometerpy.acquisition (status, transactiondate, rrnumber, area, userid, supplierid, acqtype, created_at, updated_at) values (0,"' + date + '","' + rrno + '","' +
                       transaction_area.area + '","' + str(request.user.id) + '","' + str(supplierid) + '", "' + str(acqtype) + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '", "' + now.strftime('%Y-%m-%d %H:%M:%S') + '")')
        cursor.fetchall()
        id = cursor.lastrowid
        if True:
            data = {"id":id, "msg": 'saved', 'acqtype':acqtype}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

# meters
@login_required(login_url=login_url)
def acquisition_add(request, id):
    transaction_area = userarea.objects.get(userid=request.user.id)
    acq = acquisition.objects.select_related('supplierid').values(
        'id', 'transactiondate', 'rrnumber', 'supplierid__suppliername', 'supplierid__address').get(pk=id)
    mBrand = brands.objects.order_by('brand').distinct()
    mTypes = mtype.objects.order_by('metertype').distinct()
    mAmp = meters.objects.values('Amperes').order_by('Amperes').distinct()
    mSupplier = suppliers.objects.order_by('suppliername').distinct()
    context = {'header': 'Meter Acquisition', 'datetoday': datetoday, 'acq':acq, 'area': transaction_area.area,
                'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'mBrand': mBrand, 'mTypes': mTypes, 'mAmp': mAmp, 'mSupplier': mSupplier}
    return render(request, html_mAdd, context)

def acquisition_edit(request, id):
    if request.is_ajax():
        id = request.GET.get('id')
        acqinfo = acquisition.objects.get(pk=id)
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
                                                                                            'mtypeid__metertype', 'mtypeid', 'Amperes', 'serialnos', 'units').order_by(order_by)
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
        Amperes = str(request.GET.get('Amperes'))
        serialnos = str(request.GET.get('serialnos'))
        units = str(request.GET.get('units'))

        cursor = connection.cursor()
        cursor.execute('insert into zanecometerpy.meters (acquisitionid, brandid, mtypeid, Amperes, serialnos, units) values ("' + acquisitionid + '","' + brandid + '","' + mtypeid + '","' + Amperes + '","' + serialnos + '","' + units + '")')
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

def meter_edit(request):
    if request.is_ajax():
        option = str(request.GET.get('option'))
        if (option == "locate"):
            id = str(request.GET.get('id'))
            info = meters.objects.get(pk=id)
            data = {"id": info.id, "brandid": info.brandid.id, "brand": info.brandid.brand,
                    "mtypeid": info.mtypeid.id, "metertype": info.mtypeid.metertype, "Amperes": info.Amperes, "serialnos": info.serialnos, "units": info.units}
        else:
            id = str(request.GET.get('id'))
            brandid = str(request.GET.get('brandid'))
            mtypeid = str(request.GET.get('mtypeid'))
            Amperes = str(request.GET.get('Amperes'))

            cursor = connection.cursor()
            cursor.execute("update zanecometerpy.meters set brandid = '{0}', mtypeid = '{1}', Amperes = '{2}' where id = {3}".format(
                brandid, mtypeid, Amperes, id))
            cursor.fetchall()
            data = {"msg": "updated"}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')

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

# meter seal
@login_required(login_url=login_url)
def acquisition_adds(request, id):
    transaction_area = userarea.objects.get(userid=request.user.id)
    acq = acquisition.objects.select_related('supplierid').values(
        'id', 'transactiondate', 'rrnumber', 'supplierid__suppliername', 'supplierid__address').get(pk=id)
    mBrand = brands.objects.order_by('brand').distinct()
    mSupplier = suppliers.objects.order_by('suppliername').distinct()
    context = {'header': 'Seal Acquisition', 'datetoday': datetoday, 'acq': acq, 'area': transaction_area.area,
               'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'mBrand': mBrand, 'mSupplier': mSupplier}

    return render(request, html_msAdd, context)


def seal_ss(request):
    if request.is_ajax():
        id = str(request.GET.get('id'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        cursor = connection.cursor()
        query = 'SELECT seals.id, brand, boxes, ppb, (boxes * ppb) as total, serialnos ' \
                    'FROM seals ' \
                    'LEFT JOIN brands ON (`seals`.`brandid` = `brands`.`id`) ' \
                    'WHERE acquisitionid = '+ id +' ORDER BY id ASC'
        cursor.execute(query)
        msList = cursor.fetchall()
        # print('query: ', query)
        list_data = []
        for index, item in enumerate(msList[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': len(msList),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def seal_save(request):
    if request.is_ajax():
        acquisitionid = str(request.GET.get('acquisitionid'))
        brandid = str(request.GET.get('brandid'))
        boxes = str(request.GET.get('boxes'))
        ppb = str(request.GET.get('ppb'))
        serialnos = str(request.GET.get('serialnos'))
        total = str(request.GET.get('total'))

        cursor = connection.cursor()
        cursor.execute('insert into zanecometerpy.seals (acquisitionid, brandid, boxes, ppb, serialnos) values ("' +
                       acquisitionid + '","' + brandid + '","' + boxes + '","' + ppb + '","' + serialnos + '")')
        cursor.fetchall()
        sealid = cursor.lastrowid

        serials = serialnos.split('-')

        num1 = int(serials[0])
        zerofill = len(serials[0])

        sql = "insert into zanecometerpy.sealdetails (sealid,serialno,status,active) values "
        for index in range(1, int(total) + 1):
            num = num1
            num = str(num).zfill(zerofill)
            sql += '("' + str(sealid) + '","' + num + '",0,0), '
            num1 += 1

        sql = sql[:len(sql) -2]
        cursor.execute(sql)
        cursor.fetchall()

        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def seal_delete(request):
    if request.is_ajax():
        id = int(request.GET.get('id'))
        sealinfo = seals.objects.get(id=id)
        sealinfo.delete()
        if True:
            data = {"msg": 'deleted'}
        else:
            data = {"msg": 'Not deleted'}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')


def acquisition_response(request):
    if request.is_ajax():
        response = int(request.GET.get('response'))
        acquisitionid = str(request.GET.get('id'))
        cursor = connection.cursor()
        if response == 0:
            cursor.execute("update zanecometerpy.acquisition set status = 2 where id = '{0}'".format(acquisitionid))
        else:
            cursor.execute("update zanecometerpy.acquisition set status = 4 where id = '{0}'".format(acquisitionid))
        cursor.fetchall()
        if True:
            if response == 0:
                data = {"msg": 'accepted'}
            else:
                data = {"msg": 'canceled'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

def get_meter_details(request):
    if request.is_ajax():
        id = int(request.GET.get('id'))
        action = int(request.GET.get('action'))
        transaction_area = userarea.objects.get(userid=request.user.id)
        cursor = connection.cursor()
        query = """select m.id, metercondition, count(ms.id) cnt, m.units,
                            (select count(ms.id) cnt
								FROM zanecometerpy.meterseal ms
								left join zanecometerpy.meterdetails md on md.id=ms.meterdetailsid
								left join zanecometerpy.meters m on m.id=md.meterid
								left join zanecometerpy.acquisition a on a.id = m.acquisitionid
								where a.area = '0' and md.status = 0) for_calibration,
                            (select count(ms.id) cnt
								FROM zanecometerpy.meterseal ms
								left join zanecometerpy.meterdetails md on md.id=ms.meterdetailsid
								left join zanecometerpy.meters m on m.id=md.meterid
								left join zanecometerpy.acquisition a on a.id = m.acquisitionid
								where a.area = '0' and wms_status = 2) wms_returned
                            FROM zanecometerpy.meterseal ms
                            left join zanecometerpy.meterdetails md on md.id=ms.meterdetailsid
                            left join zanecometerpy.meters m on m.id=md.meterid
                            left join zanecometerpy.acquisition a on a.id = m.acquisitionid
                            where 1 = 1
                            """
        if action == 1:
            query += """and m.acquisitionid = '{0}' """.format(id)

        query += """and a.area = '{0}' """.format(transaction_area.area)
        query += """group by metercondition """
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        cnt = cursor.fetchall()
        json_data=[]
        for result in cnt:
            json_data.append(dict(zip(row_headers,result)))
        data = {"data": json_data}
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
