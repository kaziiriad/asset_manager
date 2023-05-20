from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
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
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    joined = models.DateField()

    def __str__(self):
        return self.user.get_full_name()
    
class Device(models.Model):
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=15, choices=CHOICES)
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def update_amount(self, is_checkout):
        if is_checkout:
            self.amount -= 1
        else:
            self.amount += 1
        self.save()
    
    def __str__(self):
        return self.device_type
    
class DeviceLog(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    checkout_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    condition_on_checkout = models.TextField()
    condition_on_return = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.return_date or self.return_date > timezone.now():
            condition_on_return = "Not returned yet."
        super().save(*args, **kwargs)

    def __str__(self): 
        return f"Device: {self.device}, Employee: {self.employee}, Checkout Date: {self.checkout_date}"