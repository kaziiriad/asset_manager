from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Employee, Device, DeviceLog
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import DeviceForm, EmployeeForm


#Company lists. Might be redundant. Deal with it later.
def company_list(request):
    company = Company.objects.all()
    return render(request, 'company_list.html', {'company': company})

#shows full list of employees of a company
@login_required
def company_employee_list(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    employees = company.objects.filter(company=company)
    return render(request, 'company_detail.html', {'company': company, 'employees': employees})


#create new employee
@login_required
def create_employee(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = company 
            employee.joined = timezone.now()
            employee.save()
            return redirect('company_employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'create_employee.html', {'form': form})

#employee details.
@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})

#adds device to the database.
@login_required
def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save() 
            return redirect('company_device_list')
    else:
        form = DeviceForm()

    return render(request, 'add_device.html', {'form': form})


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

        return redirect("company_device_list")
    
    
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

        return redirect('company_device_list')

    return render(request, 'return_error.html')