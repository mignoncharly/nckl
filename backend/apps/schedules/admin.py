from django.contrib import admin
from .models import PickupRegion, PickupSchedule, LoadingDate, DropOffLocation, ShipmentSchedule


@admin.register(PickupRegion)
class PickupRegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'active')
    search_fields = ('name', 'cities')
    list_filter = ('active', 'country')


@admin.register(PickupSchedule)
class PickupScheduleAdmin(admin.ModelAdmin):
    list_display = ('region', 'start_date', 'end_date', 'active')
    list_filter = ('active', 'start_date')
    search_fields = ('region__name', 'cities', 'notes')


@admin.register(LoadingDate)
class LoadingDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'active')
    list_filter = ('active', 'date')
    search_fields = ('title', 'description')


@admin.register(DropOffLocation)
class DropOffLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'location_type', 'phone', 'whatsapp', 'active', 'sort_order')
    list_filter = ('country', 'city', 'location_type', 'active')
    search_fields = ('name', 'city', 'address', 'phone', 'whatsapp')
    list_editable = ('active', 'sort_order')


@admin.register(ShipmentSchedule)
class ShipmentScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'route', 'drop_off_location', 'latest_dropoff_at', 'departure_date', 'estimated_arrival_date', 'active')
    list_filter = ('active', 'route', 'departure_date')
    search_fields = ('title', 'notes', 'route__name', 'drop_off_location__name')
