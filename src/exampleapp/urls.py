from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from exampleapp import views

router = DefaultRouter(trailing_slash=False)
router.register("tasks", views.TaskViewSet, "task")
router.register("routes/?", views.RouteViewSet, "routes")
router.register("vehicles/?", views.VehicleViewSet, "vehicle")
router.register("repairs/?", views.RepairViewSet, "repair")
router.register('insurances/?', views.InsuranceViewSet, 'insurance')
router.register('costs/?', views.CostViewSet, 'cost')

urlpatterns = [
    re_path("", include(router.urls))
]
