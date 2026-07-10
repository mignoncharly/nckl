from django.contrib import admin
from .models import ServiceType, RouteOption, AcceptedItemCategory


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'sort_order')
    list_editable = ('active', 'sort_order')


@admin.register(RouteOption)
class RouteOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'origin_label', 'destination_label', 'transit_time_display', 'active', 'sort_order')
    list_filter = ('direction', 'active')
    search_fields = ('name', 'origin_label', 'destination_label')
    list_editable = ('active', 'sort_order')


@admin.register(AcceptedItemCategory)
class AcceptedItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_weight_kg', 'requires_battery_removed', 'route_restriction', 'active', 'sort_order')
    list_filter = ('active', 'route_restriction', 'requires_battery_removed')
    search_fields = ('name', 'description')
    list_editable = ('active', 'sort_order')
