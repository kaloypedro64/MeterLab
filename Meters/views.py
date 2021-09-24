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
from .models import meters, meterdetails, metercalibration
from .forms import meterForm, meterdetailsForm, metercalibrationForm
from django.views.generic import CreateView, FormView, RedirectView, ListView
from django.utils.dateparse import parse_datetime

# Create your views here.

datetoday = datetime.date.today()

header = 'Dashboard'
html_meterlist = 'meters/meter_list.html'
html_mAdd = "meters/meter_request_add.html"
html_mEdit = "meters/meter_request_edit.html"
html_meterdetails_data = 'meters/meterdetails_data.html'
html_metertestreport = 'meters/meter_test_report.html'

html_calibration = 'calibration/calibrate.html'

# transaction_area = ''

class MeterList(ListView):
    model = meters
    html = 'meters/meters.html'
    success_url = '/'

    def get_queryset(self):
        return self.model.objects.filter(serialnos__icontains=self.request.GET.get('filter'),
            rrnumber__icontains=self.request.GET.get('filter')).values('id', 'dateforwarded', 'rrnumber', 'brand', 'ampheres', 'metertype', 'serialnos', 'units', 'active', 'userid','area').order_by( self.request.GET.get('order_by') )

    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            # filter = request.GET.get('filter')
            # order_by = request.GET.get('order_by')
            list_data = []
            for index, item in enumerate(self.get_queryset().filter(area=transaction_area.area)[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            # request.userarea
            return HttpResponse( json.dumps(data, default=default), 'application/json' )
        else:
            return render(request, self.html, {'header': 'Meters', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})

def meters_add(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.method == "POST":
        form = meterForm(request.POST)
        if form.is_valid():
            rec = form.save()
            rec.save()

            # save meter serials for manual meter entry
            cursor = connection.cursor()
            idmeters = rec.id
            units = request.POST['units']
            now = datetime.datetime.utcnow()
            serials = request.POST['serialnos'].split('-')

            num1 = int(serials[0])
            zerofill = len(serials[0])

            for index in range(1, int(units) + 1):
                num = num1
                num = str(num).zfill(zerofill)
                cursor.execute('insert into zanecometerpy.meterdetails (idmeters, serialno, wms_status, userid, created_at, updated_at) ' +
                               'values ("' + str(idmeters) + '","' + num + '","0","' + str(request.user.id) + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '","' + now.strftime('%Y-%m-%d %H:%M:%S') + '")')
                cursor.fetchall()
                num1 += 1
        return redirect("/meters")
    else:
        form = meterForm(request.POST)
        mBrand = meters.objects.order_by('brand').distinct()
        mType = meters.objects.order_by('metertype').distinct()
        mAmp = meters.objects.order_by('ampheres').distinct()
        mSupplier = get_supplier('')
        context = {'form': form, 'header': 'Add Meter', 'datetoday': datetoday, 'area': transaction_area.area,
                   'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'mBrand': mBrand, 'mType': mType, 'mAmp': mAmp, 'mSupplier': mSupplier}
        return render(request, html_mAdd, context)

def meters_edit(request, id):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.method == "POST":
        queryset = meters(pk=id)
        form = meterForm(request.POST, instance=queryset)
        print(form.is_valid)
        if form.is_valid():
            created = request.POST.get('created_at')
            rec = form.save(commit=False)
            rec.created_at = datetoday
            rec.save()
            # form.save()
        return redirect("/meters")
    else:
        queryset = meters.objects.get(pk=id)
        mBrand = meters.objects.values('brand').order_by('brand').distinct()
        mType = meters.objects.values('metertype').order_by('metertype').distinct()
        mAmp = meters.objects.values('ampheres').order_by('ampheres').distinct()
        print('amp', mAmp.query)
        context = {'form': queryset, 'header': 'Edit Meter',
                   'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'mBrand': mBrand, 'mType': mType, 'mAmp': mAmp}
        return render(request, html_mEdit, context)

def meters_delete(request, id):
    if request.is_ajax():
        id = request.GET.get('id')
        meterinfo = meters.objects.get(pk=id)
        meterinfo.delete()

        # meterinfo_details = meterdetails.objects.get(idmeters=id)
        # meterinfo_details.delete()


        json_response = {json.dumps('deleted')}
    return HttpResponse(json_response, content_type='application/json')

def meters_detail(request, id):
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        query = meterdetails.objects.select_related('meters').filter(idmeters=id,
            serialno__icontains=filter,).values('id', 'idmeters', 'serialno',
                                                'accuracy', 'wms_status', 'status', 'active', 'userid', 'idmeters__brand').order_by(order_by)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')
    else:
        return render(request, 'meters/meterdetails.html', {'idmeters': id, 'header': 'Meter Details'})

def meter_selected(request):
    if request.is_ajax():
        id = request.GET.get('id')
        idmeters = request.GET.get('idmeters')
        queryset = metercalibration.objects.filter(idmeterdetails=id).order_by('idmeterdetails')
        context = {'trans': queryset, 'id': id, 'idmeters': idmeters}
        return render(request, html_meterdetails_data, context)

# SET FOREIGN_KEY_CHECKS=0;
# SET GLOBAL FOREIGN_KEY_CHECKS=0;


def calibrate(request, id, idmeters):
    if request.method == "POST":
        form = metercalibrationForm(request.POST)
        if form.is_valid():
            # print('saved', form.data)
            form.save()
            idmeterdetails = request.POST['idmeterdetails']
            average = request.POST['gen_average']
            cursor = connection.cursor()
            cursor.execute('update zanecometerpy.meterdetails set wms_status=1, status = if("' + str(
                average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(id) + '"')
            cursor.fetchall()
            return redirect("../../")
        else:
            data = {"err_msg": form.errors}
            return JsonResponse(data)
    else:
        serials = meterdetails.objects.get(id=id)
        form = metercalibrationForm(request.POST)
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': idmeters}
        return render(request, html_calibration, context)


def get_supplier(o):
    if o:
        cursor = connection.cursor()
        cursor.execute(
            'select distinct idsupplier, suppliername, address from zanecoinvphp.tbl_supplier where idsupplier = "'+ o +'" order by suppliername asc')
        suppliers = cursor.fetchall()
        return JsonResponse(suppliers, content_type='application/json')
    else:
        cursor = connection.cursor()
        cursor.execute('select distinct idsupplier, suppliername, address from zanecoinvphp.tbl_supplier order by suppliername asc')
        suppliers = cursor.fetchall()
        return suppliers #json.dumps(suppliers, default=default)

# def edit_meters(request, id, idmeters):
#     if request.method == "POST":
#         queryset = meterserials_details(pk=id)
#         form = metercalibrationForm(request.POST, instance=queryset)
#         if form.is_valid():
#             created = request.POST.get('created_at')
#             print(parse_datetime(created))
#             rec = form.save(commit=False)
#             rec.created_at = datetoday
#             rec.save()

#             cursor = connection.cursor()
#             idmeterdetails = request.POST['idmeterdetails']
#             average = request.POST['gen_average']
#             cursor.execute(
#                 'update zanecometerpy.meter_serials set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(idmeterdetails) + '"')
#             cursor.fetchall()
#         return redirect("../../")
#     else:
#         queryset = meterserials_details.objects.get(pk=id)
#         serials = meterserials.objects.get(id=idmeters)
#         # serials = meterserials.objects.select_related(
#         #     "meter_serials").filter(id=idmeters)
#         context = {'form': queryset, 'datetoday': datetoday, 'serials': serials}
#         return render(request, 'meters/calibration_edit.html', context)

# multiple calibration
def calibrate_multiple(request, id):
    html = 'calibration/calibration_multiple.html'
    serials = meterdetails.objects.filter(idmeters=id).filter(wms_status__exact=0)
    form = metercalibrationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            idmeterdetails = request.POST['idmeterdetails']
            average = request.POST['gen_average']
            cursor = connection.cursor()
            cursor.execute(
                'update zanecometerpy.meter_serials set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(idmeterdetails) + '"')
            cursor.fetchall()
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': id, 'save': 'save'}
        return render(request, html, context)
    else:
        form = metercalibrationForm(request.POST)
        # serials = meterserials.objects.filter(idmeters=id).filter(wms_status__exact=0)
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': id}
        return render(request, html, context)


def calibrate_delete(request, id):
    if request.is_ajax():
        id = request.GET.get('id')
        serialinfo = metercalibration.objects.get(pk=id)
        serialinfo.delete()
        json_response = {json.dumps('deleted')}
    return HttpResponse(json_response, content_type='application/json')


def meter_test_report(request, id, idmeters):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute('SELECT brand, serialno, ampheres, accuracy, msd.* FROM zanecometerpy.meter_serials_details msd ' +
                       'left join meter_serials ms on ms.id = msd.idmeterdetails ' +
                       'left join meters m on m.id=ms.idmeters ' +
                       'where msd.id = "' + str(id) + '";')
        form = cursor.fetchall()
        context = {'form': form, 'datetoday': datetoday}
    return render(request, html_metertestreport, context)


# def save_selectedTable(request):
#     if request.is_ajax():
#         id = request.GET.get('id')
#         cursor = connection.cursor()
#         cursor.execute('update zanecometerpy.meter_serials set wms_status=2 where id = "'+ str(id) +'" ')
#         cursor.fetchall()
#         return render(request, html_meterlist)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


        # form = metercalibrationForm(request.POST, instance=queryset)

        # cursor = connection.cursor()
        # cursor.execute('select idmeterdetails ' +
        #                '   from zanecometerpy.meter_serials_details ' +
        #             #    '   where idmeterdetails like "' + str(id) + '" ' +
        #                '    ;')
        # result = cursor.fetchall()
