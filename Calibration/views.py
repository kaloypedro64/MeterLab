from queue import Empty
from typing import cast
from django.http.response import HttpResponse, JsonResponse
from MeterLab.settings import AREA_CHOICES
from Signatory.models import signatory
from Users.models import userarea
import datetime
import json
from django.db import connection
from django.shortcuts import render, redirect

from Meters.models import *
from Meters.forms import *


# Create your views here.
header = 'Calibration'
datetoday = datetime.date.today()
datenow = datetime.datetime.now()
html_calibration_history = 'calibration/calibration_history.html'
html_calibration_edit = 'calibration/calibration_edit.html'
html_test_preview = 'calibration/print_test.html'
html_print_calibration_history = 'calibration/print_calibration_history.html'

html_calibration_details = 'calibration/calibration_details.html'
html_print_calibration_details = 'calibration/print_calibration_details.html'


def calibration(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.is_ajax():
        action = request.GET.get('action')
        status = int(request.GET.get('status'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        isfiltered = ''

        # status 0 and 6
        query = """
                select md.id, md.serialno,
                    (select brand from brands where id=m.brandid) brand,
                    (select metertype from metertype where id=m.mtypeid) metertype,
                 amperes, ms.accuracy, md.status,
                 ms.transactiondate, metercondition, reading, seal_a, seal_b, metertype,
                 wms_status
                from meters m
                inner join acquisition a on a.id = m.acquisitionid and a.status <> 1
                left join metertype mt on mt.id = m.mtypeid
                left join meterdetails md on m.id = md.meterid
                -- left join auth_user_area ua on ua.userid = a.userid
                left join meterseal ms on ms.meterdetailsid = md.id
                """

        if filter:
            isfiltered = "and ( md.serialno like '%" + filter + "%' ) "
        if status == '':
            status = 0
        cursor = connection.cursor()
        query += "where md.status = " + str(status) + " " + isfiltered
        query += "and a.area = " + str(transaction_area.area)

        if date_from:
            query += " and ms.transactiondate between '{0}' and '{1}'".format(date_from, date_to)

        if action == 'history':
            query += " and ms.transactiondate is not null "
            query += " order by md.updated_at desc"
        else:
            query += " order by cast(md.serialno as SIGNED) asc"

        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        cnt = cursor.fetchall()

        json_data = []
        for result in cnt:
            json_data.append(dict(zip(row_headers, result)))

        # mList = cursor.fetchall()

        list_data = []
        for index, item in enumerate(json_data[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': len(cnt),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')
    else:
        context = {'datetoday': datetoday, 'header': 'Calibration',
                   'transaction_area': AREA_CHOICES[int(transaction_area.area)]}
        return render(request, html_calibration_history, context)


def calibrate_edit(request, id):
    if request.method == "POST":
        queryset = metertest(pk=id)
        form = metertestForm(request.POST, instance=queryset)
        if form.is_valid():

            rec = form.save(commit=False)
            rec.updated_at = datenow
            rec.save()
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
        transaction_area = userarea.objects.get(userid=request.user.id)
        query = """select sd.id, sd.serialno
                        from sealdetails sd
                        left join seals s on s.id = sd.sealid
                        left join acquisition a on a.id = s.acquisitionid
                        where a.area = '{0}' and serialno like '%{1}%' and active = 0
                        order by cast(serialno AS UNSIGNED INTEGER)""".format(transaction_area.area, search)
        cursor = connection.cursor()
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        cnt = cursor.fetchall()

        json_data=[]
        for result in cnt:
            json_data.append(dict(zip(row_headers,result)))

        list_data = []
        datas = []
        for index, item in enumerate(json_data):
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
        transaction_area = userarea.objects.get(userid=request.user.id)
        query = """SELECT md.id, md.serialno
                    FROM meterdetails md
                    left join meters m on m.id = md.meterid
                    left join acquisition a on a.id = m.acquisitionid
                        where a.area = '{0}' and serialno like '%{1}%' and active = 0 and md.status = 0
                        order by cast(serialno AS UNSIGNED INTEGER)""".format(transaction_area.area, search)
        cursor = connection.cursor()
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        cnt = cursor.fetchall()

        json_data=[]
        for result in cnt:
            json_data.append(dict(zip(row_headers,result)))

        list_data = []
        datas = []
        for index, item in enumerate(json_data):
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
                'update zanecometerpy.meterdetails set status = 2, updated_at = now() where id like "' + meterdetailsid + '"; ' + \
                'insert into zanecometerpy.meterseal (transactiondate, seal_a, seal_b, metercondition, accuracy, reading, remarks, meterdetailsid, userid) ' + \
                       'values ("' + transactiondate + '","' + seal_a + '","' + seal_b + '","' + metercondition + '","' + accuracy + '","' + reading + '","' + remarks + '","' + meterdetailsid + '","' + str(request.user.id) + '")'
        cursor.execute(query)
        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')


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


def print_calibration_history(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    signs = signatory.objects.filter(area=transaction_area.area).first()
    date_from = request.GET.get('range')
    d_range = date_from.split('|')

    isfiltered = ''

    # status 0 and 6
    query = """
            select md.id, md.serialno,
                (select brand from brands where id=m.brandid) brand,
                (select metertype from metertype where id=m.mtypeid) metertype,
                Amperes, ms.accuracy, md.status,
                ms.transactiondate, metercondition, ms.accuracy, reading, seal_a, seal_b, metertype
            from meters m
            inner join acquisition a on a.id = m.acquisitionid
            left join metertype mt on mt.id = m.mtypeid
            left join meterdetails md on m.id = md.meterid
            -- left join auth_user_area ua on ua.userid = a.userid
            left join meterseal ms on ms.meterdetailsid = md.id
            """

    cursor = connection.cursor()
    query += "where md.status = 2 " + isfiltered
    query += "and a.area = " + str(transaction_area.area)
    query += " and ms.transactiondate between '{0}' and '{1}'".format(
        d_range[0], d_range[1])
    query += " and ms.transactiondate is not null "
    # query += " group by md.serialno order by cast(md.serialno as SIGNED) asc, transactiondate desc"
    query += " group by md.serialno order by ms.transactiondate desc"
    cursor.execute(query)
    mList = cursor.fetchall()
    context = {'mList': mList, 'signs': signs, 'date_from': d_range[0], 'date_to': d_range[1]}
    return render(request, html_print_calibration_history, context)


def return_meters_one_by_one(request):
    if request.is_ajax():
        id = request.GET.get('id')
        cursor = connection.cursor()
        query = """ update meterdetails set wms_status = 2, rtw_at = now() where id = '{0}' and status <> 0 """.format(id)
        cursor.execute(query)
        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

def return_meters_by_range(request):
    if request.is_ajax():
        serial = request.GET.get('range')
        s_range = serial.split('-')
        cursor = connection.cursor()
        query = """ update meterdetails set wms_status = 2, rtw_at = now() where serialno between '{0}' and '{1}' and status <> 0 """.format(s_range[0], s_range[1])
        cursor.execute(query)
        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def calibration_details(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.is_ajax():
        status = int(request.GET.get('status'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        isfiltered = ''

        # status 0 and 6
        cursor = connection.cursor()
        query = """
                select md.id, md.serialno,
                    (select brand from brands where id=m.brandid) brand,
                    (select metertype from metertype where id=m.mtypeid) metertype,
                 Amperes, ms.accuracy, md.status,
                 ms.transactiondate, metercondition, ms.accuracy, reading, seal_a, seal_b, metertype,
                 wms_status
                from meters m
                inner join acquisition a on a.id = m.acquisitionid and a.status <> 1
                left join metertype mt on mt.id = m.mtypeid
                left join meterdetails md on m.id = md.meterid
                left join meterseal ms on ms.meterdetailsid = md.id
                where 1 = 1
                """

        if filter:
            isfiltered = " and ( md.serialno like '%" + filter + "%' ) "
        if status == '':
            status = 0
        if status <= 3:
            query += " and ms.metercondition = " + str(status)
        query += isfiltered
        query += " and a.area = " + str(transaction_area.area)

        if date_from:
            query += " and ms.transactiondate between '{0}' and '{1}' ".format(date_from, date_to)
        query += " and ms.transactiondate is not null "
        cursor.execute(query)

        row_headers = [x[0] for x in cursor.description]
        cnt = cursor.fetchall()

        json_data = []
        for result in cnt:
            json_data.append(dict(zip(row_headers, result)))

        list_data = []
        for index, item in enumerate(json_data[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': len(cnt),
            'objects': list_data,
        }
        # print('data', data)
        return HttpResponse(json.dumps(data, default=default), 'application/json')
    else:
        context = {'datetoday': datetoday, 'header': 'Calibration Details',
                   'transaction_area': AREA_CHOICES[int(transaction_area.area)]}
        return render(request, html_calibration_details, context)


def print_calibration_details(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    signs = signatory.objects.filter(area=transaction_area.area).first()
    status = int(request.GET.get('status'))
    date_from = request.GET.get('range')
    d_range = date_from.split('|')

    isfiltered = ''

    # status 0 and 6
    query = """
            select md.id, md.serialno,
                (select brand from brands where id=m.brandid) brand,
                (select metertype from metertype where id=m.mtypeid) metertype,
                Amperes, ms.accuracy, md.status,
                ms.transactiondate, metercondition, ms.accuracy, reading, seal_a, seal_b, metertype
            from meters m
            inner join acquisition a on a.id = m.acquisitionid
            left join metertype mt on mt.id = m.mtypeid
            left join meterdetails md on m.id = md.meterid
            left join auth_user_area ua on ua.userid = a.userid
            left join meterseal ms on ms.meterdetailsid = md.id
            where 1= 1
            """

    cursor = connection.cursor()
    query += " and md.status = 2 " + isfiltered
    query += " and ua.area = " + str(transaction_area.area)
    query += " and ms.transactiondate between '{0}' and '{1}'".format(d_range[0], d_range[1])
    query += " and ms.transactiondate is not null "
    if status <= 3:
        query += " and ms.metercondition = " + str(status)
    query += " group by md.serialno order by ms.transactiondate desc"
    cursor.execute(query)

    mList = cursor.fetchall()
    context = { 'mList': mList, 'signs': signs,
               'date_from': d_range[0], 'date_to': d_range[1], 'status': status }
    return render(request, html_print_calibration_details, context)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
