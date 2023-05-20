from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Employee, Device, DeviceLog
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.utils import timezone

#Company lists. Might be redundant. Deal with it later.
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})

#shows full list of employees of a company
@login_required
def company_employee_list(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    employees = company.objects.filter(company=company)
    return render(request, 'company_detail.html', {'company': company, 'employees': employees})

#employee details.
@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})

#List of devices each company has.
@login_required
def company_device_list(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    devices = company.objects.filter(owner=company)
    return render(request, 'device_list.html', {'company': company, 'devices': devices})

#device details/logs.
@login_required
def device_detail(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device_logs = device.devicelog_set.all()
    return render(request, 'device_detail.html', {'device': device, 'device_logs': device_logs})

#device checkout.
@login_required 
def checkout_device(request, device_id, employee_id):

    device = get_object_or_404(Device, id=device_id)
    employee = get_object_or_404(Employee, id=employee_id)
    
    if device.amount > 0 and device.owner == employee.company:
        device.update_amount(is_checkout=True)
        device_log = DeviceLog.object.create(
            device=device,
            employee=employee,
            checkout_date=timezone,
            condition_on_checkout="Good"
        )

        return redirect("device_list_url")
    
    
    return render(request, "checkout_error.html")

@login_required
def return_device(request, log_id):
    device_log = get_object_or_404(DeviceLog, id=log_id)

    if not device_log.return_date or self.return_date <= timezone.now():

        device_log.return_date = timezone.now()
        device_log.condition_on_return = "Good"
        device_log.save()

        device = device_log.device
        device.update_amount(is_checkout=False)

        return redirect('device_list_url')

    return render(request, 'return_error.html')