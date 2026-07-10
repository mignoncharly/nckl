from rest_framework import serializers
from .models import ServiceType, RouteOption, AcceptedItemCategory
from apps.core.i18n import is_admin_request, translate_database_value


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'name', 'description', 'icon')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not is_admin_request(self):
            data['name'] = translate_database_value(data['name'])
            data['description'] = translate_database_value(data['description'])
        return data


class AdminServiceTypeSerializer(ServiceTypeSerializer):
    class Meta(ServiceTypeSerializer.Meta):
        fields = ServiceTypeSerializer.Meta.fields + ('active', 'sort_order')


class RouteOptionSerializer(serializers.ModelSerializer):
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)

    class Meta:
        model = RouteOption
        fields = (
            'id', 'name', 'direction', 'direction_display', 'origin_label',
            'destination_label', 'transit_time_display', 'shopping_assistance_available',
            'notes',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not is_admin_request(self):
            for field in ('name', 'origin_label', 'destination_label', 'transit_time_display', 'notes'):
                data[field] = translate_database_value(data.get(field, '') or '')
        return data


class AdminRouteOptionSerializer(RouteOptionSerializer):
    class Meta(RouteOptionSerializer.Meta):
        fields = RouteOptionSerializer.Meta.fields + ('active', 'sort_order', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class AcceptedItemCategorySerializer(serializers.ModelSerializer):
    route_restriction_display = serializers.CharField(source='get_route_restriction_display', read_only=True)

    class Meta:
        model = AcceptedItemCategory
        fields = (
            'id', 'name', 'description', 'max_weight_kg', 'requires_battery_removed',
            'route_restriction', 'route_restriction_display',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not is_admin_request(self):
            data['name'] = translate_database_value(data['name'])
            data['description'] = translate_database_value(data['description'])
        return data


class AdminAcceptedItemCategorySerializer(AcceptedItemCategorySerializer):
    class Meta(AcceptedItemCategorySerializer.Meta):
        fields = AcceptedItemCategorySerializer.Meta.fields + ('active', 'sort_order', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
