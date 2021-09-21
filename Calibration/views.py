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

from Meters.models import meters, meterdetails, metercalibration, meterseal
from Meters.forms import meterForm, meterdetailsForm, metercalibrationForm, metersealForm

from django.views.generic import CreateView, FormView, RedirectView, ListView
from django.utils.dateparse import parse_datetime

# Create your views here.
class CalibrationList(ListView):
    model = meterdetails
    html = 'calibration/calibration_list.html'
    success_url = '/'

    def get_queryset(self):
        return self.model.objects.select_related('meters', 'meterseal', 'metercalibration').filter(serialno__icontains=self.request.GET.get('filter'),).values('id',
            'idmeters', 'serialno', 'ampheres', 'accuracy', 'wms_status', 'status', 'active', 'userid', 'idmeters__brand', 'idmeters__metertype',
            'meterseal__seal_a', 'meterseal__seal_b', 'metercalibration__testdate').order_by(self.request.GET.get('order_by'))

    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            list_data = []
            print('response', self.get_queryset().query)
            for index, item in enumerate(self.get_queryset().filter(status__isnull=False)[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            # request.userarea
            return HttpResponse( json.dumps(data, default=default), 'application/json' )
        else:
            return render(request, self.html, {'header': 'Calibration', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
