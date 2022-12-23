import logging

from exampleapp import models, serializers
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Return information about task.
    """
    serializer_class = serializers.TaskSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = models.Task.objects.all()

    def create(self, request):
        """
        Submit a new task.
        """
        task_serializer = serializers.TaskSerializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)

        logging.info("Creating task")
        # task submit
        task = models.Task()
        task.description = request.data.get("description")
        task.save()
        logging.info("Task created")

        return Response({"msg": "Task created"}, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        List all the tasks.
        """
        qs = models.Task.objects.all()
        task_serializer = serializers.TaskSerializer(qs, many=True)

        return Response(task_serializer.data, status=status.HTTP_200_OK)


# class RepairViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.RepairSerializer
#     # permission_classes = (IsAuthenticated,)
#     queryset = models.Repair.objects.all()
#
#     def create(self, request):
#         task_serializer = serializers.RepairSerializer(data=request.data)
#         task_serializer.is_valid(raise_exception=True)
#
#         logging.info("Creating repair")
#
#         repair = models.Repair()
#         repair.description = request.data.get("description")
#         repair.repair_date = request.data.get("repair_date")
#         repair.vehicle = request.data.get("vin")
#         repair.save()
#         logging.info("Repair created")
#
#         return Response({'msg': 'Repair created'}, status=status.HTTP_201_CREATED)
#
#     def list(self, request):
#         qs = models.Repair.objects.all()
#         repair_serializer = serializers.RepairSerializer(qs, many=True)
#
#         return Response(repair_serializer.data, status=status.HTTP_200_OK)


class VehicleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Vehicle.objects.all()
    serializer_class = serializers.VehicleSerializer

    def create(self, request, *args, **kwargs):

        _serializer = self.serializer_class(data=request.data)
        _serializer.is_valid(raise_exception=True)

        logging.info("Creating vehicle")

        vehicle = models.Vehicle()
        vehicle.vin = request.data.get("vin")
        vehicle.year_of_production = request.data.get("year_of_production")
        vehicle.car_review = request.data.get("car_review")
        vehicle.fuel_usage = request.data.get("fuel_usage")
        vehicle.kilometers_done = request.data.get("kilometers_done")

        vehicle.save()
        logging.info("Vehicle created")

        return Response(data=_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        qs = models.Vehicle.objects.all()
        vehicle_serializer = serializers.VehicleSerializer(qs, many=True)

        return Response(vehicle_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        _serializer = self.serializer_class(vehicle)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        vehicle.delete()
        return Response({'message': 'Vehicle has been deleted successfully'}, status=status.HTTP_200_OK)


class RepairViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Repair.objects.all()
    serializer_class = serializers.RepairSerializer

    def create(self, request, *args, **kwargs):
        queryset = models.Vehicle.objects.all()

        vehicle = get_object_or_404(queryset, pk=request.data.get("vin"))
        data = {
            'description': request.data.get('description'),
            'vehicle': vehicle.pk
        }
        _serializer = self.serializer_class(data=data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Repair.objects.all()
        repair_serializer = serializers.RepairSerializer(qs, many=True)

        return Response(repair_serializer.data, status=status.HTTP_200_OK)


class CostViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Cost.objects.all()
    serializer_class = serializers.CostSerializer

    def create(self, request, *args, **kwargs):
        queryset = models.Repair.objects.all()

        repair = get_object_or_404(queryset, pk=request.data.get("vin"))
        data = {
            'description': request.data.get('description'),
            'vehicle': vehicle.pk
        }
        _serializer = self.serializer_class(data=data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Repair.objects.all()
        repair_serializer = serializers.RepairSerializer(qs, many=True)

        return Response(repair_serializer.data, status=status.HTTP_200_OK)