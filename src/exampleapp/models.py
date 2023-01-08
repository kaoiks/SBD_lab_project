from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text="user full name")
    role = models.CharField(max_length=32, blank=True, null=True, help_text="user role")

    def __str__(self):
        return self.name


class Task(models.Model):
    description = models.CharField(max_length=128, help_text="Task description")


class Vehicle(models.Model):
    vin = models.CharField(max_length=64, primary_key=True, unique=True)
    year_of_production = models.IntegerField()
    car_review = models.DateField()
    fuel_usage = models.FloatField()
    kilometers_done = models.IntegerField()


class Repair(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='repairs', default=None, on_delete=models.CASCADE)
    repair_date = models.DateField(auto_now_add=True, blank=True, null=False)
    description = models.TextField(default="", blank=True, null=False)


class Cost(models.Model):
    repair = models.ForeignKey(Repair, related_name='repair_costs', on_delete=models.CASCADE)
    date = models.DateField()
    invoice_id = models.CharField(max_length=100, unique=True)
    amount = models.FloatField()


class Insurance(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='insurances', default=None, on_delete=models.CASCADE)
    insurance_number = models.TextField(primary_key=True, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.FloatField()


class Address(models.Model):
    street = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=140)

    ADDRESS_TYPE_CHOICES = [
        (1, _('Contractor')),
        (2, _('Driver'))
    ]
    type = models.CharField(choices=ADDRESS_TYPE_CHOICES, max_length=20, null=False, blank=False)

    class Meta:
        unique_together = (('street', 'postal_code', 'city', 'type'),)


class Contractor(models.Model):
    nip = models.CharField(primary_key=True, max_length=10, unique=True)
    name = models.CharField(max_length=256)
    country_id = models.CharField(max_length=2)
    address = models.OneToOneField(Address, related_name='address', null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('nip', 'address'),)


class Invoice(models.Model):
    contractor = models.ForeignKey(Contractor, related_name='invoices', default=None, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True, blank=False, null=False)
    date = models.DateField()
    amount = models.FloatField()


class Driver(models.Model):
    pesel = models.CharField(primary_key=True, max_length=11, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    driver_license_number = models.CharField(max_length=100, unique=True)
    date_qualification_certificate = models.DateField()
    date_bhp_course = models.DateField()
    address = models.OneToOneField(Address, related_name='address_driver', null=False, blank=False, on_delete=models.CASCADE)


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    date = models.DateField()
    begin = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    distance = models.IntegerField()
    driver = models.ForeignKey(Driver, related_name='driver', null=True, blank=True, on_delete=models.DO_NOTHING)
    contractor = models.ForeignKey(Contractor, related_name='contractor', null=False, blank=False, on_delete=models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, related_name='vehicle', on_delete=models.DO_NOTHING)


class Settlement(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    saturdays = models.IntegerField()
    days_stationary = models.IntegerField()
    days_leave = models.IntegerField()
    rate_for_kilometer = models.FloatField()
    kilometers_done = models.IntegerField()
    driver = models.ForeignKey(Driver, related_name='settlements', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (('month', 'year', 'driver'),)