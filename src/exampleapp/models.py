from django.db import models


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
    invoice_id = models.CharField(max_length=100)
    amount = models.FloatField()


class Insurance(models.Model):
    insurance_number = models.TextField(primary_key=True, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.FloatField()


class Address(models.Model):
    street = models.TextField()
    postal_code = models.TextField()


class Contractor(models.Model):
    nip = models.IntegerField()

    country_id = models.TextField(max_length=2)


