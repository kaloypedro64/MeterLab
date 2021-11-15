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
html_metertestreport = 'meters/meter_test_report.html'

html_calibration = 'calibration/calibrate.html'
html_mcalibration = 'calibration/calibration_multiple.html'


# transaction_area = ''


# def MeterList(request):
#     html = 'meters/meters.html'
#     transaction_area = userarea.objects.get(userid=request.user.id)
#     if request.is_ajax():
#         start = int(request.GET.get('start'))
#         limit = int(request.GET.get('limit'))
#         filter = request.GET.get('filter')
#         order_by = request.GET.get('order_by')
#         print('order_by', order_by)

#         cursor = connection.cursor()
#         query = 'SELECT id, dateforwarded, rrnumber, suppliername, address, brand, ampheres, metertype, serialnos, units, active, userid, area FROM meters m left join zanecoinvphp.tbl_supplier s on s.idsupplier = m.supplierid;'
#         cursor.execute(query)
#         # col_names = [desc[0] for desc in cursor.description]
#         # col_name = col_names[abs(float(order_by))]

#         isfiltered = ''
#         if filter:
#             isfiltered = " and ( name like '%" + filter + "%'  or address like '%" + \
#                 filter + "%' or ordate like '%" + filter + "%')"


#         query = 'SELECT id, dateforwarded, rrnumber, suppliername, address, brand, ampheres, metertype, serialnos, units, active, userid, area ' + \
#                     'FROM meters m ' + \
#                     'left join zanecoinvphp.tbl_supplier s on s.idsupplier = m.supplierid ' + \
#                     'where 1=1 ' + isfiltered + ' order by ' + order_by
#         cursor.execute(query)
#         mList = cursor.fetchall()
#         list_data = []
#         for index, item in enumerate(mList[start:start+limit], start):
#             list_data.append(item)
#         data = {
#             'length': len(mList),
#             'objects': list_data,
#         }
#         return HttpResponse(json.dumps(data, default=default), 'application/json')
#     else:
#         return render(request, html, {'header': 'Meters', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})

# @login_required(login_url='/')
class meterList(ListView):
    model = meters
    html = 'meters/meters.html'

    def get_queryset(self):
        return self.model.objects.select_related('brand', 'mtype', 'acquisition').values('id', 'acquisitionid', 'acquisitionid__transactiondate', 'brandid__brand',
                                                                                         'mtypeid__metertype', 'mtypeid', 'ampheres', 'serialnos', 'units', 'acquisitionid__area').order_by(self.request.GET.get('order_by'))
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
            return HttpResponse(json.dumps(data, default=default), 'application/json')
        else:
            return render(request, self.html, {'header': 'Meters', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})


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

# # SET FOREIGN_KEY_CHECKS=0;
# # SET GLOBAL FOREIGN_KEY_CHECKS=0;


def calibrate(request, id):
    if request.method == "POST":
        form = metertestForm(request.POST)
        if form.is_valid():
            form.save()
            meterdetailsid = request.POST['meterdetailsid']
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


# def get_supplier():
#     cursor = connection.cursor()
#     cursor.execute(
#         'select distinct idsupplier, suppliername, address from zanecoinvphp.tbl_supplier order by suppliername asc')
#     suppliers = cursor.fetchall()
#     return suppliers  # json.dumps(suppliers, default=default)

# # multiple calibration


def calibrate_multiple(request, id):
    html = 'calibration/calibration_multiple.html'
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
        return render(request, html, context)
    else:
        # serials = meterserials.objects.filter(idmeters=id).filter(wms_status__exact=0)
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': id}
        return render(request, html, context)





def calibration_history(request):
    html = 'calibration/calibration_history.html'
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        # if (order_by)
        # query = metertest.objects.select_related('brand', 'meters', 'meterdetails').filter(meterdetailsid__serialno__icontains=filter,
        #                                                                                    ).values('id', 'meterdetailsid__serialno', 'meterdetailsid', 'testdate', 'gen_average',
        #                                                                                             'brandid__brand', 'fl1', 'fl2', 'fl3',
        #                                                                                                     'lightload_average', 'll1', 'll2', 'll3',
        #                                                                                                     'reading', 'type', 'volts', 'phase', 'kh', 'ta', 'remarks',
        #                                                                                                     'active', 'isdamage',).order_by(order_by)
        # return self.model.objects.select_related('meters', 'meterseal', 'metercalibration').filter(serialno__icontains=self.request.GET.get('filter'),).values('id',
        #                                                                                                                                                        'idmeters', 'serialno', 'ampheres', 'accuracy', 'wms_status', 'status', 'active', 'userid', 'idmeters__brand', 'idmeters__metertype',
        #                                                                                                                                                        'meterseal__seal_a', 'meterseal__seal_b', 'metercalibration__testdate').order_by(self.request.GET.get('order_by'))

        # list_data = []
        # for index, item in enumerate(query[start:start+limit], start):
        #     list_data.append(item)
        # data = {
        #     'length': query.count(),
        #     'objects': list_data,
        # }

        # query = 'select md.id, mt.testdate, md.serialno, ' + \
        #         '    (select brand from brands where id=m.brandid) brand, ' + \
        #         '    (select metertype from metertype where id=m.mtypeid) metertype, ' + \
        #         ' md.status, reading, accuracy, ' + \
                # '    (select serialno from sealdetails where meterdetailsid=md.id limit 1) seriala, ' +
                # '    (select serialno from sealdetails where meterdetailsid=md.id order by id desc limit 1) serialb, ' + \
                # ' ampheres, mt.id metertestid ' + \
                # 'from metertest mt ' + \
                # 'left join meterdetails md on md.id = mt.meterdetailsid ' + \
                # 'left join meters m on m.id = md.meterid ';

        cursor = connection.cursor()
        query = 'select md.id, mt.testdate, md.serialno, ' + \
                '    (select brand from brands where id=m.brandid) brand, ' + \
                '    (select metertype from metertype where id=m.mtypeid) metertype, ' + \
                ' ampheres, accuracy, md.status, reading, ' + \
                ' mt.id metertestid ' + \
                'from metertest mt ' + \
                'left join meterdetails md on md.id = mt.meterdetailsid ' + \
                'left join meters m on m.id = md.meterid ';
        cursor.execute(query)
        # col_names = [desc[0] for desc in cursor.description]
        # col_name = col_names[abs(float(order_by))]

        isfiltered = ''
        if filter:
            isfiltered = " and ( or md.serialno like '%" + \
                filter + "%' or mt.testdate like '%" + filter + "%') "
                # "having brand like '%" + filter + "%' "

        query += 'where 1 = 1 ' + isfiltered;
        # order by mt.' + order_by;

        # print('query', query)
        cursor.execute(query)
        mList = cursor.fetchall()
        list_data = []
        for index, item in enumerate(mList[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': len(mList),
            'objects': list_data,
        }

        return HttpResponse(json.dumps(data, default=default), 'application/json')
    else:
        test = metertest.objects.all()
        context = {'datetoday': datetoday, 'test': test}
        return render(request, html, context)

# load data to select option - serverside dropdown
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


def consumer_search(request):
    if request.is_ajax():
        id = request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute('SELECT idnewapply id, name, address, ordate, ornumber FROM zanecoisd.newapply ' +
                       'where idnewapply = "' + str(id) + '";')
        form = cursor.fetchall()
    return HttpResponse(json.dumps(form, default=default), 'application/json')


def consumer_save_assignedmeter(request):
    if request.is_ajax():
        meterdetailsid = str(request.GET.get('meterdetailsid'))
        metertestid = str(request.GET.get('metertestid'))
        consumerid = str(request.GET.get('consumer'))

        cursor = connection.cursor()
        cursor.execute('SELECT idnewapply id, name, address, ordate, ornumber, ratecode FROM zanecoisd.newapply ' +
                       'where idnewapply = "' + str(consumerid) + '";')
        consumer = cursor.fetchall()

        name = consumer[0][1]
        address = consumer[0][2]
        ratecode = consumer[0][5]
        cursor.execute('insert into zanecometerpy.assigned_meter (transactiondate, metertestid, meterdetailsid, consumer, address, type, userid) ' +
                       'values ("' + str(metertestid) + '","' + str(metertestid) + '","' + str(meterdetailsid) + '","' + name + '","' + address + '","' + ratecode + '","' + str(request.user.id) + '")')
        cursor.fetchall()

        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

# def calibrate_single(request, id):
#     html = 'calibration/calibration.html'
#     serials = meterdetails.objects.filter(
#         meterid=id).filter(wms_status__exact=0)
#     form = metertestForm(request.POST)
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             meterid = request.POST['idmeterdetails']
#             average = request.POST['gen_average']
#             cursor = connection.cursor()
#             cursor.execute(
#                 'update zanecometerpy.meterdetails set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(meterid) + '"')
#             cursor.fetchall()
#         context = {'form': form, 'datetoday': datetoday,
#                    'serials': serials, 'idmeters': id, 'save': 'save'}
#         return render(request, html, context)
#     else:
#         form = metertestForm(request.POST)
#         # serials = meterserials.objects.filter(idmeters=id).filter(wms_status__exact=0)
#         context = {'form': form, 'datetoday': datetoday,
#                    'serials': serials, 'idmeters': id}
#         return render(request, html, context)

# def calibrate_delete(request, id):
#     if request.is_ajax():
#         id = request.GET.get('id')
#         serialinfo = calibration.objects.get(pk=id)
#         serialinfo.delete()
#         json_response = {json.dumps('deleted')}
#     return HttpResponse(json_response, content_type='application/json')


# def meter_test_report(request, id, idmeters):
#     if request.method == "GET":
#         cursor = connection.cursor()
#         cursor.execute('SELECT brand, serialno, ampheres, accuracy, msd.* FROM zanecometerpy.meter_serials_details msd ' +
#                        'left join meter_serials ms on ms.id = msd.idmeterdetails ' +
#                        'left join meters m on m.id=ms.idmeters ' +
#                        'where msd.id = "' + str(id) + '";')
#         form = cursor.fetchall()
#         context = {'form': form, 'datetoday': datetoday}
#     return render(request, html_metertestreport, context)


# def save_selectedTable(request):
#     if request.is_ajax():
#         id = request.GET.get('id')
#         cursor = connection.cursor()
#         cursor.execute('update zanecometerpy.meter_serials set wms_status=2 where id = "'+ str(id) +'" ')
#         cursor.fetchall()
#         return render(request, html_meterlist)

# serverside
# def meterdetails_ss(request, id):
#     if request.is_ajax():
#         start = int(request.GET.get('start'))
#         limit = int(request.GET.get('limit'))
#         filter = request.GET.get('filter')
#         order_by = request.GET.get('order_by')
#         query = meterdetails.objects.select_related('meters').filter(idmeters=id,
#                                                                      serialno__icontains=filter,).values('id', 'idmeters', 'serialno', 'ampheres',
#                                                                                                          'accuracy', 'wms_status', 'status', 'active', 'userid', 'idmeters__brand').order_by(order_by)
#         list_data = []
#         for index, item in enumerate(query[start:start+limit], start):
#             list_data.append(item)
#         data = {
#             'length': query.count(),
#             'objects': list_data,
#         }
#         return HttpResponse(json.dumps(data, default=default), 'application/json')
#     else:
#         return render(request, 'meters/meterdetails.html', {'idmeters': id, 'header': 'Meter Details'})

def load_assigned_consumers(request, id):
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        query = assigned_meter.objects.filter(meterdetailsid=id, consumer__icontains=filter,).values(
            'id', 'transactiondate', 'meterdetailsid', 'consumer', 'address', 'type', 'active', 'userid').order_by(order_by)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')

# def expire_page_cache(view, args=None):
#     """
#     Removes cache created by cache_page functionality.
#     Parameters are used as they are in reverse()
#     """

#     if args is None:
#         path = reverse(view)
#     else:
#         path = reverse(view, args=args)

#     request = HttpRequest()
#     request.path = path
#     key = get_cache_key(request)
#     if cache.has_key(key):
#         cache.delete(key)

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
