import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render
from MeterLab.settings import AREA_CHOICES
from django.views.generic import CreateView, FormView, RedirectView, ListView

from Meters.models import suppliers
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
        return self.model.objects.order_by(self.request.GET.get('order_by'))

    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            filter = request.GET.get('filter')
            list_data = []
            for index, item in enumerate(self.get_queryset()[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            return HttpResponse(json.dumps(data, default=default), 'application/json')
        else:
            return render(request, self.html, {'header': 'Meters', 'datetoday': datetoday, 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
