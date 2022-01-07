from typing import cast
from django.http.response import HttpResponse, JsonResponse
from MeterLab.settings import AREA_CHOICES
from Users.models import userarea
import datetime
import json
from django.db import connection
from django.db.models.expressions import Window
from django.shortcuts import render, redirect

from Meters.models import *
from Meters.forms import *

from django.views.generic import CreateView, FormView, RedirectView, ListView
from django.utils.dateparse import parse_datetime, postgres_interval_re

# Create your views here.
header = 'Calibration'
datetoday = datetime.date.today()
datenow = datetime.datetime.now()
html_calibration_history = 'calibration/calibration_history.html'
html_calibration_edit = 'calibration/calibration_edit.html'
html_test_preview = 'calibration/print_test.html'


# class Calibration(ListView):
#     model = meterdetails
#     html = 'calibration/calibration_history.html'
#     success_url = '/'

#     def get_queryset(self):
#         query = 'select md.id, md.serialno, ' + \
#                 '    (select brand from brands where id=m.brandid) brand,' + \
#                 '    (select metertype from metertype where id=m.mtypeid) metertype,' + \
#                 ' ampheres, accuracy, md.status ' + \
#                 'from meters m ' + \
#                 'left join meterdetails md on m.id = md.meterid '
#         return query

#     def get(self, request, *args, **kwargs):
#         transaction_area = userarea.objects.get(userid=request.user.id)
#         query = self.get_queryset()
#         if request.is_ajax():
#             status = int(request.GET.get('status'))
#             start = int(request.GET.get('start'))
#             limit = int(request.GET.get('limit'))
#             filter = request.GET.get('filter')
#             order_by = request.GET.get('order_by')

#             isfiltered = ''
#             if filter:
#                 isfiltered = " and ( md.serialno like '%" + filter + "%' ) "

#             cursor = connection.cursor()
#             # query += 'where status = '+ status +' '+ isfiltered
#             query += 'where status = 0 ' + isfiltered

#             cursor.execute(query)
#             mList = cursor.fetchall()

#             print('query', query)

#             list_data = []
#             for index, item in enumerate(mList[start:start+limit], start):
#                 list_data.append(item)
#             data = {
#                 'length': len(mList),
#                 'objects': list_data,
#             }
#             return HttpResponse(json.dumps(data, default=default), 'application/json')
#         else:
#             context = {'datetoday': datetoday, 'header': 'Calibration',
#                        'transaction_area': AREA_CHOICES[int(transaction_area.area)]}
#             return render(request, self.html, context)


def calibration(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.is_ajax():
        status = int(request.GET.get('status'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        isfiltered = ''

        query = 'select md.id, md.serialno, ' + \
                '    (select brand from brands where id=m.brandid) brand,' + \
                '    (select metertype from metertype where id=m.mtypeid) metertype,' + \
                ' ampheres, accuracy, md.status ' + \
                'from meters m ' + \
                'inner join acquisition a on a.id = m.acquisitionid ' + \
                'left join meterdetails md on m.id = md.meterid '

        if filter:
            isfiltered = " and ( md.serialno like '%" + filter + "%' ) "
        if status == '':
            status = 0
        # print('status', status)
        cursor = connection.cursor()
        query += "where md.status = " + str(status) + " " + isfiltered
        # query += 'where status = 0 ' + isfiltered

        cursor.execute(query)
        mList = cursor.fetchall()

        # print("query", query)
        list_data = []
        for index, item in enumerate(mList[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': len(mList),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')
    else:
        # serials = meterdetails.objects.all()
        context = {'datetoday': datetoday, 'header': 'Calibration', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]}
        return render(request, html_calibration_history, context)

def calibrate_edit(request, id):
    if request.method == "POST":
        queryset = metertest(pk=id)
        form = metertestForm(request.POST, instance=queryset)
        if form.is_valid():

            rec = form.save(commit=False)
            rec.updated_at = datenow

            rec.save()
            # meterid = request.POST['meterdetailsid']
            # average = request.POST['gen_average']
            # cursor = connection.cursor()
            # cursor.execute(
            #     'update zanecometerpy.meterdetails set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(meterid) + '"')
            # cursor.fetchall()
            return redirect("/calibration")
        else:
            data = {"err_msg": form.errors}
            return JsonResponse(data)

    else:
        queryset = metertest.objects.get(pk=id)
        serials = meterdetails.objects.get(pk=queryset.meterdetailsid.id)

        context = {'form': queryset, 'serials': serials,'idmeters': id}
        return render(request, html_calibration_edit, context)

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

def seal_list(request):
    if request.is_ajax():
        search = request.GET.get('searchTerm')
        query = sealdetails.objects.filter(serialno__icontains=search, active__icontains=0).extra(select={'serialnos': 'cast(serialno AS UNSIGNED INTEGER)'}).values('id', 'sealid', 'meterdetailsid',
                                                                               'serialno', 'techcrew', 'status', 'active').order_by('serialnos')
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

def meters_list(request):
    if request.is_ajax():
        search = request.GET.get('searchTerm')
        query = meterdetails.objects.filter(serialno__icontains=search, active__icontains=0, status=0).values('id', 'meterid', 'serialno', 'accuracy', 'wms_status', 'status', 'active').order_by('serialno')
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

# assigning meter to consumer
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
        transactiondate = str(request.GET.get('transactiondate'))
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
                       'values ("' + str(transactiondate) + '","' + str(metertestid) + '","' + str(meterdetailsid) + '","' + name + '","' + address + '","' + ratecode + '","' + str(request.user.id) + '")')
        cursor.fetchall()

        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

# put seal on meter
def calibration_update_save(request):
    if request.is_ajax():
        # ismulti = str(request.GET.get('ismulti'))
        meterdetailsid = str(request.GET.get('meterdetailsid'))
        transactiondate = str(request.GET.get('transactiondate'))
        seal_a = str(request.GET.get('seal_a'))
        seal_b = str(request.GET.get('seal_b'))
        metercondition = str(request.GET.get('metercondition'))
        accuracy = str(request.GET.get('accuracy'))
        reading = str(request.GET.get('reading'))
        remarks = str(request.GET.get('remarks'))

        cursor = connection.cursor()
        query = 'update zanecometerpy.sealdetails set active = 1 where serialno like "' + seal_a + '"; ' + \
                'update zanecometerpy.sealdetails set active = 1 where serialno like "' + seal_b + '"; ' + \
                'update zanecometerpy.meterdetails set status = 2 where id like "' + meterdetailsid + '"; ' + \
                'insert into zanecometerpy.meterseal (transactiondate, seal_a, seal_b, metercondition, accuracy, reading, remarks, meterdetailsid, userid) ' + \
                       'values ("' + transactiondate + '","' + seal_a + '","' + seal_b + '","' + metercondition + '","' + accuracy + '","' + reading + '","' + remarks + '","' + meterdetailsid + '","' + str(request.user.id) + '")'

        # cursor.execute('insert into zanecometerpy.meterseal (transactiondate, seal_a, seal_b, metercondition, accuracy, reading, remarks, meterdetailsid, userid) ' +
        #                'values ("' + transactiondate + '","' + seal_a + '","' + seal_b + '","' + metercondition + '","' + accuracy + '","' + reading + '","' + remarks + '","' + meterdetailsid + '","' + str(request.user.id) + '")')
        # cursor.fetchall()

        cursor.execute(query)

        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

# def load_assigned_consumers(request, id):
#     if request.is_ajax():
#         start = int(request.GET.get('start'))
#         limit = int(request.GET.get('limit'))
#         filter = request.GET.get('filter')
#         order_by = request.GET.get('order_by')
#         query = assigned_meter.objects.filter(meterdetailsid=id, consumer__icontains=filter,).values(
#             'id', 'transactiondate', 'meterdetailsid', 'consumer', 'address', 'type', 'active', 'userid').order_by(order_by)
#         list_data = []
#         for index, item in enumerate(query[start:start+limit], start):
#             list_data.append(item)
#         data = {
#             'length': query.count(),
#             'objects': list_data,
#         }
#         return HttpResponse(json.dumps(data, default=default), 'application/json')

def dt_meterseal_details(request, id):
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        query = meterseal.objects.filter(meterdetailsid=id, seal_a__icontains=filter, seal_b__icontains=filter, remarks__icontains=filter,).values(
            'id', 'transactiondate', 'seal_a',
                  'seal_b', 'metercondition', 'accuracy', 'reading', 'remarks', 'active', 'userid', 'meterdetailsid').order_by(order_by)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')



def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
