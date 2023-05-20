from django import forms
from .models import Device, Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'company', 'joined']
        exclude = ('user',)
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name', 'device_type', 'owner', 'amount'] 