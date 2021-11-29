from cryptography.fernet import Fernet
from MeterLab.views import call_key, genwrite_key
from decimal import Decimal
from MeterLab.settings import AREA_CHOICES
from Users.models import userarea
from Users.forms import AreaForm
import datetime
import json
from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request

from Meters.models import *
from Meters.forms import *



# Create your views here.

datetoday = datetime.date.today()

def AssignedList(request):
    html = 'assign/assign.html'
    success_url = '/'
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')

        cursor = connection.cursor()
        # query = 'SELECT idnewapply id, name, address, ordate, "From I" as type, ornumber FROM zanecoisd.newapply where ornumber is not null'
        # cursor.execute(query)
        # col_names = [desc[0] for desc in cursor.description]
        # col_name = col_names[abs(int(order_by))]

        isfiltered = ''
        if filter:
            isfiltered = " and ( name like '%" + filter + "%'  or address like '%" + \
                filter + "%' or datepaid like '%" + filter + "%')"

        #if sorted
        sortby = "desc"
        num1 = int(order_by)
        if num1 <= 0:
            sortby = "asc"
        # query = 'SELECT idnewapply id, name, address, ordate, "From I" as type, ornumber FROM zanecoisd.newapply where ornumber is not null '+ isfiltered +' order by ' + col_name + ' ' + sortby
        query = 'select * from ' + \
                '(  ' + \
                '    (select idnewconnection as idtrans, ' + \
                '        name, ' + \
                '        address, ' + \
                '        "New Connection" as description, ' + \
                '        date_format(DatePaid, '"'%Y-%m-%d'"') DatePaid, ' + \
                '        ORNumber, ' + \
                '        1 as transcode, ' + \
                '        accountnumber ' + \
                '            from zanecoisd.newconnection ' + \
                '    where ifnull(trim(ornumber),'"''"') <> '"''"' and  ' + \
                '                   ifnull(trim(serial),'"''"') = '"''"' and  ' + \
                '                   ifnull(name,'"''"') <> '"''"' and  ' + \
                '                   ifnull(Accomplished,'"''"') = 0 and  ' + \
                '                   datepaid>'"'2013-12-31'"') ' + \
                'union all ' + \
                '(select idrecon as idtrans, ' + \
                '        name, ' + \
                '        address, ' + \
                '        "Reconnection" as description, ' + \
                '        date_format(ORDate, '"'%Y-%m-%d'"') ORDate, ' + \
                '        ORNumber, ' + \
                '        2 as transcode, ' + \
                '        accountnumber ' + \
                '            from zanecoisd.recon ' + \
                '   where ifnull(trim(ornumber),'"''"') <> '"''"' and ' + \
                '                 ifnull(trim(serial),'"''"') = '"''"' and ' + \
                '                 ifnull(name,'"''"') <> '"''"' and ' + \
                '                 ifnull(Accomplished,'"''"') = 0 and ' + \
                '                 recondate>'"'2013-12-31'"') ' + \
            ') trans where 1=1 '+ \
            isfiltered + \
            'order by datepaid desc;'
        cursor.execute(query)
        coname = cursor.fetchall()

        list_data = []
        # print('list_data', query)

        for index, item in enumerate(coname[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': len(coname),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')
    else:
        return render(request, html, {'header': 'Calibration', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})


def assign(request, str):
    transaction_area = userarea.objects.get(userid=request.user.id)
    form = meterassignedForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            rec = form.save()
            rec.save()
        return redirect("..")
    else:

        serials = calibration.objects.select_related(
            'idmeterdetails').filter().values('id', 'idmeterdetails__serialno')
        # print('get', name)
        context = {'form': form, 'header': 'Meter Assign',
                   'datetoday': datetoday, 'serials': serials, 'coname': str}
        return render(request, "assign/assign_add.html", context)

def assign_selected(request):
    if request.is_ajax():
        id = request.GET.get('id')
        # assign = meterassignedForm(request.POST)
        print('id',id)
        query = metercalibration.objects.select_related(
            'idmeterdetails').filter().values('id', 'idmeterdetails__serialno')
        # json_response = {json.dumps(query, cls=DecimalEncoder)}
        # print('res2', json_response)
    # return JsonResponse(query, content_type='application/json')
    # return JsonResponse({'assign': assign, 'calibrated_meter': query})
    return render(request, 'assign/modal_assign.html', {'assign': assign, 'calibrated_meter': query})

def selected_serialno(request):
    if request.is_ajax():
        id = request.GET.get('id')
        query = meterdetails.objects.select_related('idmeters', 'metercalibration').filter(
            metercalibration__id=id).values('id', 'idmeters__brand', 'metercalibration__reading')
        json_response = {json.dumps(query[0], cls=DecimalEncoder)}
    return HttpResponse(json_response, content_type='application/json')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return {
                "_type": "decimal",
                "value": str(obj)
            }
        return super(DecimalEncoder, self).default(obj)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
