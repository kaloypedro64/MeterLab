import datetime
import json
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from Calibration.views import print_calibration_history
from MeterLab.settings import AREA_CHOICES
from django.views.generic import CreateView, FormView, RedirectView, ListView
from django.core.serializers.json import DjangoJSONEncoder
from Meters.forms import supplierForm
from django.views.decorators.csrf import csrf_exempt
from Meters.models import acquisition, suppliers
from Users.models import userarea

# Create your views here.
datetoday = datetime.date.today()
datenow = datetime.datetime.now()

html_suppliers = 'suppliers/suppliers.html'



# @login_required(login_url='/')
class SuppliersList(ListView):
    model = suppliers
    html = html_suppliers

    def get_queryset(self):
        return self.model.objects.values('id', 'suppliername', 'address').order_by(self.request.GET.get('order_by'))

    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            filter = request.GET.get('filter')
            list_data = []
            # print('self.get_queryset()', self.get_queryset().query)
            for index, item in enumerate(self.get_queryset()[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            return HttpResponse(json.dumps(data, default=default), 'application/json')
        else:
            return render(request, self.html, {'header': 'Suppliers', 'datetoday': datetoday, 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})


def getSupplierDetails(request):
    if request.is_ajax():
        id = int(request.GET.get('id'))
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        cursor = connection.cursor()
        query = """select a.transactiondate, a.rrnumber,
                        (select brand from brands where id=m.brandid) brand,
                        (select metertype from metertype where id=m.mtypeid) metertype,
                        units, serialnos
                    from acquisition a
                    inner join meters m on m.acquisitionid = a.id
                         where a.supplierid = '{0}' """.format(id)
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
        return HttpResponse(json.dumps(data, default=default), 'application/json')


# @csrf_exempt
def saveSupplier(request):
    if request.is_ajax():
        form = supplierForm(request.POST)
        if form.is_valid():
            rec = form.save()
            rec.save()
        if True:
            data = {"msg": 'saved'}
        else:
            data = {"msg": 'Not saved'}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

def editSupplier(request):
    if request.method == "POST":
        id = str(request.POST.get('id'))
        queryset = suppliers(pk=id)
        form = supplierForm(request.POST, instance=queryset)
        if form.is_valid():
            rec = form.save(commit=False)
            # rec.updated_at = datenow
            rec.save()
            data = {"msg": "updated"}
            return JsonResponse(data)
        else:
            data = {"err_msg": form.errors}
            return JsonResponse(data)

    else:
        id = str(request.GET.get('id'))
        queryset = suppliers.objects.get(pk=id)
        # print('data', queryset.suppliername)
        data = {'id': queryset.id, 'suppliername': queryset.suppliername,
                'address': queryset.address}
        return HttpResponse(json.dumps(data, default=default), 'application/json')

# @csrf_exempt
def delSupplier(request):
    if request.is_ajax():
        id = int(request.GET.get('id'))
        sealinfo = suppliers(id=id)
        sealinfo.delete()
        if True:
            data = {"msg": 'deleted'}
        else:
            data = {"msg": 'Not deleted'}
    return HttpResponse(json.dumps(data, default=default), content_type='application/json')

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
