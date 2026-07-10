from rest_framework import generics, permissions
from .models import ServiceType, RouteOption, AcceptedItemCategory
from .serializers import (
    ServiceTypeSerializer,
    AdminServiceTypeSerializer,
    RouteOptionSerializer,
    AdminRouteOptionSerializer,
    AcceptedItemCategorySerializer,
    AdminAcceptedItemCategorySerializer,
)
from apps.core.permissions import IsStaffOrAdmin


class ServiceTypeListView(generics.ListAPIView):
    queryset = ServiceType.objects.filter(active=True)
    serializer_class = ServiceTypeSerializer
    permission_classes = []


class RouteOptionListView(generics.ListAPIView):
    queryset = RouteOption.objects.filter(active=True).order_by('sort_order', 'name')
    serializer_class = RouteOptionSerializer
    permission_classes = []


class AcceptedItemCategoryListView(generics.ListAPIView):
    queryset = AcceptedItemCategory.objects.filter(active=True).order_by('sort_order', 'name')
    serializer_class = AcceptedItemCategorySerializer
    permission_classes = []


class AdminServiceTypeListCreateView(generics.ListCreateAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = AdminServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminServiceTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = AdminServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminRouteOptionListCreateView(generics.ListCreateAPIView):
    queryset = RouteOption.objects.all().order_by('sort_order', 'name')
    serializer_class = AdminRouteOptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminRouteOptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RouteOption.objects.all()
    serializer_class = AdminRouteOptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminAcceptedItemCategoryListCreateView(generics.ListCreateAPIView):
    queryset = AcceptedItemCategory.objects.all().order_by('sort_order', 'name')
    serializer_class = AdminAcceptedItemCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


class AdminAcceptedItemCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcceptedItemCategory.objects.all()
    serializer_class = AdminAcceptedItemCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]
