import logging

from exampleapp import models, serializers
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
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

        return Response(data=self.serializer_class(vehicle).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        qs = models.Vehicle.objects.all()
        vehicle_serializer = serializers.VehicleSerializer(qs, many=True)

        return Response(vehicle_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        _serializer = self.serializer_class(vehicle)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        vehicle.car_review = request.data.get("car_review")
        vehicle.year_of_production = request.data.get("year_of_production")
        vehicle.fuel_usage = request.data.get("fuel_usage")
        vehicle.kilometers_done = request.data.get("kilometers_done")
        vehicle.save()

        return Response(self.serializer_class(vehicle).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        vehicle.delete()
        return Response({'message': 'Vehicle has been deleted successfully'}, status=status.HTTP_200_OK)


class InsuranceViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Insurance.objects.all()
    serializer_class = serializers.InsuranceSerializer

    def create(self, request, *args, **kwargs):
        queryset = models.Vehicle.objects.all()  # NOQA
        # logging.info(f"Checking if vehicle with vin {request.data.get('vin')} exists")
        vehicle = get_object_or_404(queryset, pk=request.data.get("vin"))
        data = {
            'insurance_number': request.data.get('insurance_number'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'amount': request.data.get('amount'),
            'vehicle': vehicle.pk
        }

        _serializer = self.serializer_class(data=data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Insurance.objects.all()  # NOQA
        insurance_serializer = serializers.InsuranceSerializer(qs, many=True)

        return Response(insurance_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Insurance.objects.all()
        insurance = get_object_or_404(queryset, pk=pk)
        _serializer = self.serializer_class(insurance)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Insurance.objects.all()
        insurance = get_object_or_404(queryset, pk=pk)
        insurance.start_date = request.data.get("start_date")
        insurance.end_date = request.data.get("end_date")
        insurance.amount = request.data.get("amount")
        queryset_vehicles = models.Vehicle.objects.all()
        try:
            insurance.vehicle = get_object_or_404(queryset_vehicles, pk=request.data.get("vin"))
        except Exception:
            return Response({'message': 'Vehicle doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)
        insurance.save()

        return Response(self.serializer_class(insurance).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Insurance.objects.all()
        insurance = get_object_or_404(queryset, pk=pk)
        insurance.delete()
        return Response({'message': 'Insurance has been deleted successfully'}, status=status.HTTP_200_OK)


class RepairViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Repair.objects.all()
    serializer_class = serializers.RepairSerializer

    def create(self, request, *args, **kwargs):
        queryset = models.Vehicle.objects.all()  # NOQA

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
        qs = models.Repair.objects.all()  # NOQA
        repair_serializer = serializers.RepairSerializer(qs, many=True)

        return Response(repair_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Repair.objects.all()
        repair = get_object_or_404(queryset, pk=pk)
        _serializer = serializers.RepairSerializer(repair)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Repair.objects.all()
        repair = get_object_or_404(queryset, pk=pk)
        repair.description = request.data.get("description")

        queryset_vehicles = models.Vehicle.objects.all()
        try:
            repair.vehicle = get_object_or_404(queryset_vehicles, pk=request.data.get("vin"))
        except Exception:
            return Response({'message': 'Vehicle doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)
        repair.save()

        return Response(self.serializer_class(repair).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Repair.objects.all()
        repair = get_object_or_404(queryset, pk=pk)
        repair.delete()
        return Response({'message': 'Repair has been deleted successfully'}, status=status.HTTP_200_OK)


class CostViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Cost.objects.all()
    serializer_class = serializers.CostSerializer

    def create(self, request, *args, **kwargs):

        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Cost.objects.all()
        cost_serializer = serializers.CostSerializer(qs, many=True)

        return Response(cost_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Cost.objects.all()
        cost = get_object_or_404(queryset, pk=pk)
        _serializer = self.serializer_class(cost)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Cost.objects.all()
        cost = get_object_or_404(queryset, pk=pk)
        cost.date = request.data.get("date")
        cost.invoice_id = request.data.get("invoice_id")
        cost.amount = request.data.get("amount")

        queryset_repairs = models.Repair.objects.all()
        try:
            cost.repair = get_object_or_404(queryset_repairs, pk=request.data.get("repair"))
        except Exception:
            return Response({'message': 'Repair doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)
        cost.save()

        return Response(self.serializer_class(cost).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Cost.objects.all()
        cost = get_object_or_404(queryset, pk=pk)
        cost.delete()
        return Response({'message': 'Cost has been deleted successfully'}, status=status.HTTP_200_OK)


class AddressViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer

    def create(self, request, *args, **kwargs):

        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Address.objects.all()
        address_serializer = serializers.AddressSerializer(qs, many=True)

        return Response(address_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Address.objects.all()
        address = get_object_or_404(queryset, pk=pk)
        _serializer = self.serializer_class(address)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Address.objects.all()
        address = get_object_or_404(queryset, pk=pk)
        address.street = request.data.get("street")
        address.postal_code = request.data.get("postal_code")
        address.city = request.data.get("city")

        address.save()

        return Response(self.serializer_class(address).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Address.objects.all()
        cost = get_object_or_404(queryset, pk=pk)
        cost.delete()
        return Response({'message': 'Address has been deleted successfully'}, status=status.HTTP_200_OK)


class ContractorViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Contractor.objects.all()
    serializer_class = serializers.ContractorSerializer

    def create(self, request, *args, **kwargs):

        if models.Contractor.objects.filter(nip=request.data.get("nip")):
            return Response({"message": "Contractor with this NIP exists."},
                            status=status.HTTP_406_NOT_ACCEPTABLE)  # NOQA
        try:
            address = models.Address.objects.filter(id=request.data.get("address"))[0]
            if address.type != "1":
                return Response({"message": "Address type is not compatible."},
                                status=status.HTTP_406_NOT_ACCEPTABLE)  # NOQA
        except Exception:  # NOQA
            return Response({"message": "Address does not exist."}, status=status.HTTP_406_NOT_ACCEPTABLE)  # NOQA

        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            queryset = models.Contractor.objects.all()
            contractor = get_object_or_404(queryset, pk=request.data.get("nip"))
            _serializer = serializers.ContractorShowSerializer(contractor)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Contractor.objects.all()
        contractor_serializer = serializers.ContractorShowSerializer(qs, many=True)

        return Response(contractor_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Contractor.objects.all()
        contractor = get_object_or_404(queryset, pk=pk)
        _serializer = serializers.ContractorShowSerializer(contractor)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Contractor.objects.all()
        contractor = get_object_or_404(queryset, pk=pk)
        contractor.country_id = request.data.get("country_id")
        contractor.name = request.data.get("name")

        contractor.save()

        return Response(self.serializer_class(contractor).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Contractor.objects.all()
        contractor = get_object_or_404(queryset, pk=pk)
        contractor.delete()
        return Response({'message': 'Contractor has been deleted successfully'}, status=status.HTTP_200_OK)


class InvoiceViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer

    def create(self, request, *args, **kwargs):

        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Invoice.objects.all()
        invoice_serializer = serializers.InvoiceShowSerializer(qs, many=True)

        return Response(invoice_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Invoice.objects.all()
        invoice = get_object_or_404(queryset, pk=pk)
        _serializer = serializers.InvoiceShowSerializer(invoice)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Invoice.objects.all()
        invoice = get_object_or_404(queryset, pk=pk)

        filtered_invoice =  models.Invoice.objects.filter(invoice_number=request.data.get("invoice_number")).first()

        if filtered_invoice is None:
            invoice.amount = request.data.get("amount")
            invoice.invoice_number = request.data.get("invoice_number")
            queryset_contractors = models.Contractor.objects.all()
            try:
                invoice.contractor = get_object_or_404(queryset_contractors, pk=request.data.get("contractor"))
            except Exception:
                return Response({'message': 'Contractor doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)

            invoice.save()
            return Response(self.serializer_class(invoice).data)
        else:
            if filtered_invoice.id == int(pk):
                invoice.amount = request.data.get("amount")
                queryset_contractors = models.Contractor.objects.all()
                try:
                    invoice.contractor = get_object_or_404(queryset_contractors, pk=request.data.get("contractor"))
                except Exception:
                    return Response({'message': 'Contractor doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)
                invoice.save()
                return Response(self.serializer_class(invoice).data)
            else:
                return Response({'message': 'Invoice with this invoice numer already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Invoice.objects.all()
        invoice = get_object_or_404(queryset, pk=pk)
        invoice.delete()
        return Response({'message': 'Invoice has been deleted successfully'}, status=status.HTTP_200_OK)


class DriverViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Driver.objects.all()
    serializer_class = serializers.DriverSerializer

    def create(self, request, *args, **kwargs):
        # print(request.data.get("address"))
        try:
            address = models.Address.objects.filter(id=request.data.get("address"))[0]
            if address.type != "2":
                return Response({"message": "Address type is not compatible."},
                                status=status.HTTP_406_NOT_ACCEPTABLE)  # NOQA
        except Exception:  # NOQA
            return Response({"message": "Address does not exist."}, status=status.HTTP_406_NOT_ACCEPTABLE)  # NOQA

        _serializer = serializers.DriverCreateSerializer(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            queryset = models.Driver.objects.all()
            contractor = get_object_or_404(queryset, pk=request.data.get("pesel"))
            _serializer = serializers.DriverSerializer(contractor)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Driver.objects.all()
        driver_serializer = serializers.DriverSerializer(qs, many=True)

        return Response(driver_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Driver.objects.all()
        driver = get_object_or_404(queryset, pk=pk)
        _serializer = serializers.DriverSerializer(driver)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Driver.objects.all()
        driver = get_object_or_404(queryset, pk=pk)
        driver.name = request.data.get("name")
        driver.surname = request.data.get("surname")
        driver.date_of_birth = request.data.get("date_of_birth")
        driver.driver_license_number = request.data.get("driver_license_number")
        driver.date_qualification_certificate = request.data.get("date_qualification_certificate")
        driver.date_bhp_course = request.data.get("date_bhp_course")
        driver.date_bhp_course = request.data.get("date_bhp_course")

        driver.save()

        return Response(self.serializer_class(driver).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Driver.objects.all()
        driver = get_object_or_404(queryset, pk=pk)
        try:
            driver.delete()
            return Response({'message': 'Driver has been deleted successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Driver can\'t be deleted'}, status=status.HTTP_403_FORBIDDEN)


class RouteViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer

    def create(self, request, *args, **kwargs):

        _serializer = self.serializer_class(data=request.data)
        _serializer.is_valid(raise_exception=True)

        logging.info("Creating route")

        route = models.Route()
        route.date = request.data.get("date")
        route.begin = request.data.get("begin")
        route.end = request.data.get("end")
        route.distance = request.data.get("distance")
        queryset = models.Driver.objects.all()
        try:
            route.driver = get_object_or_404(queryset, pk=request.data.get("driver"))
        except Exception:
            route.driver = None
        queryset = models.Contractor.objects.all()
        route.contractor = get_object_or_404(queryset, pk=request.data.get("contractor"))
        queryset = models.Vehicle.objects.all()
        route.vehicle = get_object_or_404(queryset, pk=request.data.get("vehicle"))
        route.save()
        logging.info("Route created")

        return Response(data=self.serializer_class(route).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        pesel = self.request.query_params.get('driver')

        if month is None or year is None or pesel is None:
            qs = models.Route.objects.all()
            route_serializer = serializers.RouteSerializer(qs, many=True)
            return Response(route_serializer.data, status=status.HTTP_200_OK)
        else:
            qs = models.Route.objects.filter(date__year=year, date__month=month, driver__pesel=pesel)
            route_serializer = serializers.RouteSerializer(qs, many=True)
            return Response(route_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Route.objects.all()
        route = get_object_or_404(queryset, pk=pk)
        _serializer = self.serializer_class(route)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        queryset = models.Route.objects.all()
        route = get_object_or_404(queryset, pk=pk)
        route.date = request.data.get("date")
        route.begin = request.data.get("begin")
        route.end = request.data.get("end")
        route.distance = request.data.get("distance")

        queryset_vehicles = models.Vehicle.objects.all()
        try:
            route.vehicle = get_object_or_404(queryset_vehicles, pk=request.data.get("vehicle"))
        except Exception:
            return Response({'message': 'Vehicle doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)


        queryset_contractors = models.Contractor.objects.all()
        try:
            route.contractor = get_object_or_404(queryset_contractors, pk=request.data.get("contractor"))
        except Exception:
            return Response({'message': 'Contractor doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)

        queryset_drivers = models.Driver.objects.all()
        try:
            route.driver = get_object_or_404(queryset_drivers, pk=request.data.get("driver"))
        except Exception:
            return Response({'message': 'Contractor doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)

        route.save()

        return Response(self.serializer_class(route).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Route.objects.all()
        route = get_object_or_404(queryset, pk=pk)
        route.delete()
        return Response({'message': 'Route has been deleted successfully'}, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False)
    # def me(self, request):
    #     serializer = self.get_serializer_class()
    #     data = serializer(request.user).data
    #     return Response(data, status=status.HTTP_200_OK)


class SettlementViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Settlement.objects.all()
    serializer_class = serializers.SettlementSerializer

    def create(self, request, *args, **kwargs):

        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA

    def list(self, request, *args, **kwargs):
        qs = models.Settlement.objects.all()
        route_serializer = serializers.SettlementSerializer(qs, many=True)

        return Response(route_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = models.Settlement.objects.all()
        route = get_object_or_404(queryset, pk=pk)
        _serializer = self.serializer_class(route)
        return Response(data=_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = models.Settlement.objects.all()
        settlement = get_object_or_404(queryset, pk=pk)
        settlement.delete()
        return Response({'message': 'Settlement has been deleted successfully'}, status=status.HTTP_200_OK)
