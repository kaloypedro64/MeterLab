from django import forms
from django.db.models import fields
from .models import *

class supplierForm(forms.ModelForm):
    class Meta:
        model = suppliers
        fields = ['id', 'suppliername','address']
    def __init__(self, *args, **kwargs):
        super(supplierForm, self).__init__(*args, **kwargs)
        self.fields['suppliername'].required = True


class brandsForm(forms.ModelForm):
    class Meta:
        model = brands
        fields = ['id', 'brand']

    def __init__(self, *args, **kwargs):
        super(brandsForm, self).__init__(*args, **kwargs)
        self.fields['brand'].required = True


class mTypeForm(forms.ModelForm):
    class Meta:
        model = mtype
        fields = ['id', 'metertype']

    def __init__(self, *args, **kwargs):
        super(mTypeForm, self).__init__(*args, **kwargs)
        self.fields['metertype'].required = True

class acquisitionForm(forms.ModelForm):
    class Meta:
        model = acquisition
        fields = ['id', 'transactiondate', 'rrnumber', 'supplierid', 'area', 'userid']

    def __init__(self, *args, **kwargs):
        super(acquisitionForm, self).__init__(*args, **kwargs)
        self.fields['transactiondate'].required = True


class meterForm(forms.ModelForm):
    class Meta:
        model = meters
        fields = ['id', 'acquisitionid', 'brandid',
                  'mtypeid', 'ampheres', 'serialnos', 'units']
        # labels = {
        #     'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit', 'area': 'Area'
        # }
        # widgets = {
        #     'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(meterForm, self).__init__(*args, **kwargs)
        # self.fields['rrnumber'].required = False


class meterdetailsForm(forms.ModelForm):
    class Meta:
        model = meterdetails
        fields = ['id', 'meterid', 'serialno', 'accuracy', 'wms_status', 'status', 'active']
        # readonly_fields = ['created_at', 'updated_at']
        # labels = {
        #     'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit'
        # }
        # widgets = {
        #     'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(meterdetailsForm, self).__init__(*args, **kwargs)
        self.fields['serialno'].required = True

class metercalibrationForm(forms.ModelForm):
    class Meta:
        model = calibration
        fields = ['id', 'meterdetailsid', 'testdate', 'gen_average',
                  'fullload_average', 'fl1', 'fl2', 'fl3',
                  'lightload_average','ll1', 'll2', 'll3',
                  'reading', 'type', 'volts', 'phase', 'kh', 'ta', 'remarks',
                  'active', 'isdamage', 'userid']
        readonly_fields = ['created_at', 'updated_at']
        # labels = {
        #     'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit'
        # }
        # widgets = {
        #     'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(metercalibrationForm, self).__init__(*args, **kwargs)
        self.fields['idmeterdetails'].required = True


# class metersealForm(forms.ModelForm):
#     class Meta:
#         model = meterseal
#         fields = ['id', 'meterdetailsid', 'sealdate', 'seal_a',
#                   'seal_a', 'active', 'userid']
#         labels = {
#             'seal_a': 'Seal 1', 'seal_b': 'Seal 2 ', 'sealdate': 'Transaction Date'
#         }
#         widgets = {
#             'sealdate': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'sealdate', 'placeholder': 'Select a date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(metersealForm, self).__init__(*args, **kwargs)


class meterassignedForm(forms.ModelForm):
    class Meta:
        model = meterassigned
        fields = ['id', 'assigneddate', 'datepaid', 'meterdetailsid', 'accountno', 'ornumber',
                  'coname', 'coaddress', 'type', 'active', 'userid']
        # labels = {
        #     'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit', 'area': 'Area'
        # }
        widgets = {
            'assigneddate': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'assigneddate', 'placeholder': 'Select a date'}),
            'datepaid': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'datepaid', 'placeholder': 'Select a date'}),
        }

    def __init__(self, *args, **kwargs):
        super(meterassignedForm, self).__init__(*args, **kwargs)
        # self.fields['rrnumber'].required = False


