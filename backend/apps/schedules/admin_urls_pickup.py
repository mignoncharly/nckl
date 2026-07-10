from django.urls import path
from . import views, admin_views

urlpatterns = [
    path('', views.AdminPickupScheduleListCreateView.as_view(), name='admin-pickup-schedule-list'),
    path('<int:pk>/', views.AdminPickupScheduleDetailView.as_view(), name='admin-pickup-schedule-detail'),
    path('export/csv/', admin_views.ExportPickupSchedulesCSVView.as_view(), name='admin-schedule-export-csv'),
    path('import/', admin_views.ImportPickupSchedulesView.as_view(), name='admin-schedule-import'),
    path('drop-off-locations/', views.AdminDropOffLocationListCreateView.as_view(), name='admin-drop-off-location-list'),
    path('drop-off-locations/<int:pk>/', views.AdminDropOffLocationDetailView.as_view(), name='admin-drop-off-location-detail'),
    path('shipment-schedules/', views.AdminShipmentScheduleListCreateView.as_view(), name='admin-shipment-schedule-list'),
    path('shipment-schedules/<int:pk>/', views.AdminShipmentScheduleDetailView.as_view(), name='admin-shipment-schedule-detail'),
]
