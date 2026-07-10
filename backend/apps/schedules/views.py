from rest_framework import generics, permissions
from django.utils import timezone
from .models import PickupSchedule, LoadingDate, DropOffLocation, ShipmentSchedule
from .serializers import (
    PickupScheduleSerializer,
    LoadingDateSerializer,
    AdminPickupScheduleSerializer,
    AdminLoadingDateSerializer,
    DropOffLocationSerializer,
    AdminDropOffLocationSerializer,
    ShipmentScheduleSerializer,
    AdminShipmentScheduleSerializer,
)
from apps.core.permissions import IsStaffOrAdmin


class PickupScheduleListView(generics.ListAPIView):
    queryset = PickupSchedule.objects.filter(active=True).select_related('region').order_by('start_date')
    serializer_class = PickupScheduleSerializer
    permission_classes = []


class LoadingDateListView(generics.ListAPIView):
    serializer_class = LoadingDateSerializer
    permission_classes = []

    def get_queryset(self):
        return LoadingDate.objects.filter(
            active=True,
            date__gte=timezone.localdate(),
        ).order_by('date')


class DropOffLocationListView(generics.ListAPIView):
    queryset = DropOffLocation.objects.filter(active=True).order_by('sort_order', 'country', 'city', 'name')
    serializer_class = DropOffLocationSerializer
    permission_classes = []


class ShipmentScheduleListView(generics.ListAPIView):
    serializer_class = ShipmentScheduleSerializer
    permission_classes = []

    def get_queryset(self):
        return ShipmentSchedule.objects.filter(active=True).select_related(
            'route', 'drop_off_location'
        ).order_by('latest_dropoff_at', 'departure_date', 'sort_order')


class AdminPickupScheduleListCreateView(generics.ListCreateAPIView):
    queryset = PickupSchedule.objects.select_related('region').all().order_by('start_date')
    serializer_class = AdminPickupScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminPickupScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PickupSchedule.objects.select_related('region').all()
    serializer_class = AdminPickupScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminLoadingDateListCreateView(generics.ListCreateAPIView):
    queryset = LoadingDate.objects.all().order_by('date')
    serializer_class = AdminLoadingDateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminLoadingDateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoadingDate.objects.all()
    serializer_class = AdminLoadingDateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminDropOffLocationListCreateView(generics.ListCreateAPIView):
    queryset = DropOffLocation.objects.all().order_by('sort_order', 'country', 'city', 'name')
    serializer_class = AdminDropOffLocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminDropOffLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DropOffLocation.objects.all()
    serializer_class = AdminDropOffLocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminShipmentScheduleListCreateView(generics.ListCreateAPIView):
    queryset = ShipmentSchedule.objects.select_related('route', 'drop_off_location').all().order_by('latest_dropoff_at', 'departure_date')
    serializer_class = AdminShipmentScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminShipmentScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShipmentSchedule.objects.select_related('route', 'drop_off_location').all()
    serializer_class = AdminShipmentScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]
