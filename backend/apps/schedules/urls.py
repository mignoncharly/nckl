from django.urls import path
from . import views

urlpatterns = [
    path('', views.PickupScheduleListView.as_view(), name='pickup-schedule-list'),
    path('drop-off-locations/', views.DropOffLocationListView.as_view(), name='drop-off-location-list'),
    path('shipment-schedules/', views.ShipmentScheduleListView.as_view(), name='shipment-schedule-list'),
]
