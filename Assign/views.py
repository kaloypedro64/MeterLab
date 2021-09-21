from decimal import Decimal
from MeterLab.settings import AREA_CHOICES
from Users.models import userarea
from Users.forms import AreaForm
import math
import datetime
import time
import json
import json as json_util
from django.db import connection
from django.db.models.expressions import OrderBy, Window
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request

from Meters.models import meters, meterdetails, metercalibration, meterseal, meterassigned
from Meters.forms import meterForm, meterassignedForm, meterdetailsForm, metercalibrationForm, metersealForm

from django.views.generic import CreateView, FormView, RedirectView, ListView
from django.utils.dateparse import parse_datetime

from django.core.serializers.json import DjangoJSONEncoder

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
        query = 'SELECT idnewapply id, name, address, ordate, "From I" as type, ornumber FROM zanecoisd.newapply where ornumber is not null'
        cursor.execute(query)
        col_names = [desc[0] for desc in cursor.description]

        # abs -> return negative to positive
        col_name = col_names[abs(int(order_by))]
        # print('order_by', col_name)

        #if filtered
        isfiltered = ''
        if filter:
            isfiltered = " and ( name like '%" + filter + "%'  or address like '%" + \
                filter + "%' or ordate like '%" + filter + "%')"

        #if sorted
        sortby = "desc"
        num1 = int(order_by)
        if num1 <= 0:
            sortby = "asc"
        query = 'SELECT idnewapply id, name, address, ordate, "From I" as type, ornumber FROM zanecoisd.newapply where ornumber is not null '+ isfiltered +' order by ' + col_name + ' ' + sortby
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


def assign(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    form = meterassignedForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            rec = form.save()
            rec.save()

            # # save meter serials for manual meter entry
            # cursor = connection.cursor()
            # idmeters = rec.id
            # units = request.POST['units']
            # now = datetime.datetime.utcnow()
            # serials = request.POST['serialnos'].split('-')

            # num1 = int(serials[0])
            # zerofill = len(serials[0])

            # for index in range(1, int(units) + 1):
            #     num = num1
            #     num = str(num).zfill(zerofill)
            #     cursor.execute('insert into zanecometerpy.meterdetails (idmeters, serialno, wms_status, userid, created_at, updated_at) ' +
            #                    'values ("' + str(idmeters) + '","' + num + '","0","' + str(request.user.id) + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '")')
            #     cursor.fetchall()
            #     num1 += 1
        return redirect("..")
    else:
        serials = metercalibration.objects.select_related(
            'idmeterdetails').filter().values('id', 'idmeterdetails__serialno')
        # cursor = connection.cursor()
        # cursor.execute('SELECT name, address, ornumber, ordate FROM zanecoisd.newapply where ornumber is not null order by name')
        # coname = cursor.fetchall()
        # print(coname)
        context = { 'form': form, 'header': 'Meter Assign', 'datetoday': datetoday, 'serials': serials, 'coname':'' }
        return render(request, "assign/assign_add.html", context)

# def assign_selected(request):
#     if request.is_ajax():
#         id = request.GET.get('id')
#         # assign = meterassignedForm(request.POST)
#         query = metercalibration.objects.select_related(
#             'idmeterdetails').filter().values('id', 'idmeterdetails__serialno')
#         # json_response = {json.dumps(query, cls=DecimalEncoder)}
#         # print('res2', json_response)
#     # return JsonResponse(query, content_type='application/json')
#     # return JsonResponse({'assign': assign, 'calibrated_meter': query})
#     return render(request, 'assign/modal_assign.html', {'assign': assign, 'calibrated_meter': query})

def selected_serialno(request):
    if request.is_ajax():
        id = request.GET.get('id')
        query = meterdetails.objects.select_related('idmeters', 'metercalibration').filter(
            metercalibration__id=id).values('id', 'idmeters__brand', 'metercalibration__reading')
        json_response = {json.dumps(query[0], cls=DecimalEncoder)}
        # print('res2', json_response)
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
