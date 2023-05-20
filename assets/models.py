from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

CHOICES = [

    ('Laptop', 'Laptop'),
    ('Monitor', 'Monitor'),
    ('Phone', 'Phone'),
    ('Tablet', 'Tablet'),
    ('Keyboard', 'Keyboard'),
    ('Mouse', 'Mouse'),
    ('Headphone', 'Headphone'),
    ('Webcam', 'Webcam'),
    ('Softlight', 'SoftLight')
]

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    joined = models.DateField()

    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def __str__(self):
        return self.get_full_name()
    
class Device(models.Model):
    devic_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=15, choices=CHOICES)
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.device_type
    
class DeviceLog(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    checkout_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    condition_on_checkout = models.TextField()
    condition_on_return = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.return_date or self.return_date > timezone.now():
            condition_on_return = "Not returned yet."

    def __str__(self): 
        return f"Device: {self.device}, Employee: {self.employee}, Checkout Date: {self.checkout_date}"