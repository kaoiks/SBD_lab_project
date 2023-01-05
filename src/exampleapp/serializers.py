from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from exampleapp import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("name", "role")


class TaskSerializer(serializers.ModelSerializer):
    description = serializers.CharField(help_text="description")

    class Meta:
        model = models.Task
        fields = '__all__'


class CostSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=64, decimal_places=2)

    def validate(self, data):
        return data

    def create(self, validated_data):
        cost = models.Cost.objects.create(**validated_data)  # saving post object
        return cost

    class Meta:
        model = models.Cost
        fields = '__all__'


class CreateVehicleSerializer(serializers.ModelSerializer):

    vin = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = models.Vehicle
        fields = ['vin']


class InsuranceSerializer(serializers.ModelSerializer):

    def validate(self, data):
        return data

    def create(self, validated_data):
        insurance = models.Insurance.objects.create(**validated_data)  # saving post object
        return insurance

    class Meta:
        model = models.Insurance
        fields = '__all__'


class RepairSerializer(serializers.ModelSerializer):
    repair_costs = CostSerializer(many=True, read_only=True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        repair = models.Repair.objects.create(**validated_data)  # saving post object
        return repair

    class Meta:
        model = models.Repair
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    repairs = RepairSerializer(many=True, read_only=True)
    # repairs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # insurances = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    insurances = InsuranceSerializer(
        many=True,
        read_only=True,
    )
    # vin = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    # year_of_production = serializers.IntegerField(required=True)
    # car_review = serializers.DateField()
    # fuel_usage = serializers.FloatField(required=True)
    # kilometers_done = serializers.IntegerField(required=True)
    # repairs = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)

    class Meta:
        model = models.Vehicle
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    street = serializers.CharField(max_length=140)
    postal_code = serializers.CharField(max_length=10)
    ADDRESS_TYPE_CHOICES = [
        (1, _('Contractor')),
        (2, _('Driver'))
    ]
    type = serializers.ChoiceField(choices=ADDRESS_TYPE_CHOICES, allow_blank=False)

    def validate(self, data):
        return data

    def create(self, validated_data):
        address = models.Address.objects.create(**validated_data)  # saving post object
        return address

    class Meta:
        model = models.Address
        fields = ('id', 'street', 'city', 'postal_code', 'type')


class InvoiceSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=64, decimal_places=2)

    def validate(self, data):
        return data

    def create(self, validated_data):
        contractor = models.Invoice.objects.create(**validated_data)  # saving post object
        return contractor

    class Meta:
        model = models.Invoice
        fields = '__all__'


class InvoiceListSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=64, decimal_places=2)

    def validate(self, data):
        return data

    def create(self, validated_data):
        contractor = models.Invoice.objects.create(**validated_data)  # saving post object
        return contractor

    class Meta:
        model = models.Invoice
        fields = ('id', 'amount', 'invoice_number', 'date')


class ContractorShowSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    invoices = InvoiceListSerializer(read_only=True, many=True)

    class Meta:
        model = models.Contractor
        fields = '__all__'


class ContractorSerializer(serializers.ModelSerializer):
    nip = serializers.CharField(max_length=10, min_length=10)

    def validate(self, data):
        return data

    def create(self, validated_data):
        contractor = models.Contractor.objects.create(**validated_data)  # saving post object
        return contractor

    class Meta:
        model = models.Contractor
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):

    def validate(self, data):
        return data

    def create(self, validated_data):
        route = models.Route.objects.create(**validated_data)  # saving post object
        return route

    class Meta:
        model = models.Route
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):

    def validate(self, data):
        return data

    def create(self, validated_data):
        contractor = models.Driver.objects.create(**validated_data)  # saving post object
        return contractor

    class Meta:
        model = models.Driver
        fields = '__all__'
