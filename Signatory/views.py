import math
import datetime
import json
import json as json_util
from django.db import connection
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request

from Users.models import userarea
from .models import *
from .forms import *

from django.views.generic import CreateView, FormView, RedirectView, ListView

# Create your views here.


class Signs(FormView):
    form_class = signatoryForm
    success_url = '/'
    template_name = 'signatory/signatory.html'

    def form_valid(self, form):
        request = self.request
        sign = form.save(commit=False)
        sign.save()
        return super().form_valid(sign)


def Signatories(request):
    transaction_area = userarea.objects.get(userid=request.user.id)
    if request.method == "POST":
        id = request.POST['id']
        if id == '':
            form = signatoryForm(request.POST)
        else:
            sign = signatory.objects.get(id=id)
            form = signatoryForm(request.POST, instance=sign)
        if form.is_valid():
            form.save()
        return redirect("../../")
    else:
        form = signatory
        if form:
            form = signatory.objects.filter(
                area=transaction_area.area).all().first()
        template_name = 'signatory/signatory.html'
        context = { 'form': form, 'transaction_area': transaction_area.area }
        return render(request, template_name, context)

