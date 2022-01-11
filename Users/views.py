from django.forms.widgets import NullBooleanSelect
from MeterLab.settings import AREA_CHOICES
import datetime
import json
import json as json_util
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as dj_login, logout
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView
from django.views.generic.list import ListView
from django.contrib.auth.hashers import make_password
# from .models import users
from .forms import *
from .models import *
# Create your views here.

datetoday = datetime.date.today()


class UserList(ListView):
    model = User
    html = 'users/users.html'
    success_url = '/'

    def get_queryset(self):
        return self.model.objects.select_related('userarea').filter(username__icontains=self.request.GET.get('filter'),).values(
            'id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'userarea__area', 'userarea__designation'
        ).order_by(self.request.GET.get('order_by'))
    def get(self, request, *args, **kwargs):
        transaction_area = userarea.objects.get(userid=request.user.id)
        if request.is_ajax():
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            list_data = []
            # print('users', self.get_queryset().query)
            for index, item in enumerate(self.get_queryset()[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            # request.userarea
            return HttpResponse(json.dumps(data, default=default), 'application/json')
        else:
            return render(request, self.html, {'header': 'Users', 'transaction_area': AREA_CHOICES[int(transaction_area.area)]})



def login(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']

            user = authenticate(request, username=cd['username'], password=cd['password'])
            # user = authenticate(
            #     request, username=cd['username'])

            if user is not None:
                if user.is_active:
                    dj_login(request, user)
                    return render(request, 'acquisitions/acquisitions.html', {'user': user, 'username': username})
                else:
                    return HttpResponse("Disabled Account")
            else:
                return render(request, 'base/login.html', {"msg": "Invalid Login"})
        else:
            return render(request, 'base/login.html', { "msg":"Invalid Login"})
    else:
        return render(request, 'base/login.html')

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user)

            # save area
            userid = user.id
            area = request.POST['area_field']
            username = request.POST['username']
            designation = request.POST['username']
            p1 = request.POST['password1']

            cursor = connection.cursor()
            cursor.execute('insert into zanecometerpy.auth_user_area (userid, area, user, designation, up) values ("' +
                           str(userid) + '","' + area + '","' + username + '","' + designation + '","' + p1 + '")')
            form = cursor.fetchall()
            #  end save area

            return render(request, 'base/login.html')
        else:
            context = {'msg': form.errors}
            return render(request, 'base/register.html', context )
    else:
        context = { 'form': UserForm, 'area': AreaForm }
        return render(request, 'base/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

def edit_users(request, id):
    queryset = User(pk=id)
    form = MyUserChangeForm(request.POST, instance=queryset)
    if request.method == "POST":
        un = request.POST.get('username')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        # print('na post', form.data)
        if p1 != p2:
            # print('dli equal', p1)
            data = {"err_msg": "Password does not match."}
            return JsonResponse(data)
        else:
            queryset.set_password(p1)
            if form.is_valid():
                # created = request.POST.get('created_at')
                rec = form.save(commit=False)
                rec.username = un
                rec.password = make_password(p1)
                rec.save()
                dj_login(request, rec)
               # save area
                userid = rec.id
                area = request.POST['area_field']
                username = request.POST['username']
                designation = request.POST['designation']

                # up = make_password(p1)
                up = p1
                # print('unsay area', up)

                cursor = connection.cursor()
                cursor.execute('update zanecometerpy.auth_user_area set area = "' + area + '", user = "' + username + '", designation = "' + designation + '", up = "' + up + '" where userid = "' + str(userid) + '"')
                form = cursor.fetchall()
                #  end save area

                return redirect("/users/list")
            else:
                data = {"err_msg": form.errors}
                return JsonResponse(data)
    else:
        queryset = User.objects.get(pk=id)
        transaction_area = userarea.objects.get(userid=request.user.id)
        form_ex = userarea.objects.get(userid=id)
        context = {'form': queryset, 'header': 'Edit Meter',
                   'transaction_area': AREA_CHOICES[int(transaction_area.area)], 'form_ex': form_ex,
                   'err_msg': ''}
        return render(request, "users/edit_user.html", context)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
