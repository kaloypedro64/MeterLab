from django import forms
from .models import meters, meterdetails, metercalibration, meterseal, meterassigned


class meterForm(forms.ModelForm):
    class Meta:
        model = meters
        fields = ['id', 'dateforwarded', 'rrnumber', 'brand',
                  'metertype', 'serialnos', 'units', 'active', 'userid', 'area']
        labels = {
            'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit', 'area': 'Area'
        }
        widgets = {
            'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        }

    def __init__(self, *args, **kwargs):
        super(meterForm, self).__init__(*args, **kwargs)
        self.fields['rrnumber'].required = False


class meterdetailsForm(forms.ModelForm):
    class Meta:
        model = meterdetails
        fields = ['id', 'idmeters', 'serialno', 'ampheres',
                  'accuracy', 'wms_status', 'status', 'active', 'userid']
        readonly_fields = ['created_at', 'updated_at']
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
        model = metercalibration
        fields = ['id', 'idmeterdetails', 'testdate', 'gen_average',
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


class metersealForm(forms.ModelForm):
    class Meta:
        model = meterseal
        fields = ['id', 'idmeterdetails', 'sealdate', 'seal_a',
                  'seal_a', 'active', 'userid']
        labels = {
            'seal_a': 'Seal 1', 'seal_b': 'Seal 2 ', 'sealdate': 'Transaction Date'
        }
        widgets = {
            'sealdate': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'sealdate', 'placeholder': 'Select a date'}),
        }

    def __init__(self, *args, **kwargs):
        super(metersealForm, self).__init__(*args, **kwargs)


class meterassignedForm(forms.ModelForm):
    class Meta:
        model = meterassigned
        fields = ['id', 'assigneddate', 'datepaid', 'idmeterdetails', 'accountno', 'ornumber',
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


