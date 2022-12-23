from rest_framework import serializers

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


class CreateVehicleSerializer(serializers.ModelSerializer):

    vin = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = models.Vehicle
        fields = ['vin']


class VehicleSerializer(serializers.ModelSerializer):
    repairs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # vin = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    # year_of_production = serializers.IntegerField(required=True)
    # car_review = serializers.DateField()
    # fuel_usage = serializers.FloatField(required=True)
    # kilometers_done = serializers.IntegerField(required=True)
    #repairs = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)

    class Meta:
        model = models.Vehicle
        fields = '__all__'


class RepairSerializer(serializers.ModelSerializer):
    repair_costs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        repair = models.Repair.objects.create(**validated_data)  # saving post object
        return repair

    class Meta:
        model = models.Repair
        fields = '__all__'


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cost
        fields = '__all__'
