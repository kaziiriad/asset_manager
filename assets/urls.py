from django.urls import path
from . import views

urlpatterns = [
    path(
        'company/', 
        views.company_list, 
        name='company_list'
    ),

    path(
        'company/<int:company_id>/', 
        views.company_employee_list, 
        name='company_employee_list'
    ),
    
    path(
        'company/<int:company_id>/create_employee/', 
        views.create_employee, 
        name='create_employee'
    ),
    
    path(
        'employee/<int:employee_id>/', 
        views.employee_detail, 
        name='employee_detail'
    ),
    
    path(
        'add_device/', 
        views.add_device, 
        name='add_device'
    ),
    
    path(
        'company/<int:company_id>/devices/', 
        views.company_device_list, 
        name='company_device_list`'
    ),
    
    path(
        'device/<int:device_id>/', 
        views.device_detail, 
        name='device_detail'
    ),
    
    path(
        'device/<int:device_id>/checkout/<int:employee_id>/', 
        views.checkout_device, 
        name='checkout_device'
    ),
    
    path(
        'device/log/<int:log_id>/return/', 
        views.return_device, 
        name='return_device'
    ),
]
