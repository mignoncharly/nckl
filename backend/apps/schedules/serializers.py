from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import PickupSchedule, LoadingDate, PickupRegion, DropOffLocation, ShipmentSchedule
from apps.core.i18n import is_admin_request, translate_database_value
from apps.services.serializers import RouteOptionSerializer


class PickupScheduleSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    cities = serializers.SerializerMethodField()

    class Meta:
        model = PickupSchedule
        fields = ('id', 'region_name', 'cities', 'start_date', 'end_date', 'notes')

    def get_cities(self, obj):
        return obj.cities or obj.region.cities


class AdminPickupScheduleSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = PickupSchedule
        fields = ('id', 'region_name', 'title', 'cities', 'start_date', 'end_date', 'notes', 'active')

    def validate(self, attrs):
        if self.instance is None and not (attrs.get('region_name') or '').strip():
            raise serializers.ValidationError({'region_name': _('This field is required.')})
        return attrs

    def _resolve_region(self, region_name, cities):
        region, _created = PickupRegion.objects.get_or_create(
            name=region_name.strip(),
            defaults={'cities': cities or ''},
        )
        return region

    def create(self, validated_data):
        region_name = validated_data.pop('region_name')
        validated_data['region'] = self._resolve_region(region_name, validated_data.get('cities', ''))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        region_name = validated_data.pop('region_name', None)
        if region_name and region_name.strip():
            validated_data['region'] = self._resolve_region(
                region_name, validated_data.get('cities', instance.cities)
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['region_name'] = instance.region.name if instance.region else ''
        return data


class LoadingDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadingDate
        fields = ('id', 'date', 'title', 'description')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not is_admin_request(self):
            data['title'] = translate_database_value(data['title'])
            data['description'] = translate_database_value(data['description'])
        return data


class AdminLoadingDateSerializer(LoadingDateSerializer):
    class Meta(LoadingDateSerializer.Meta):
        fields = LoadingDateSerializer.Meta.fields + ('active',)


class DropOffLocationSerializer(serializers.ModelSerializer):
    location_type_display = serializers.CharField(source='get_location_type_display', read_only=True)

    class Meta:
        model = DropOffLocation
        fields = (
            'id', 'name', 'city', 'country', 'location_type', 'location_type_display',
            'address', 'details', 'phone', 'whatsapp', 'opening_hours',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not is_admin_request(self):
            for field in ('name', 'city', 'country', 'address', 'details', 'opening_hours'):
                data[field] = translate_database_value(data.get(field, '') or '')
        return data


class AdminDropOffLocationSerializer(DropOffLocationSerializer):
    class Meta(DropOffLocationSerializer.Meta):
        fields = DropOffLocationSerializer.Meta.fields + ('active', 'sort_order', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class ShipmentScheduleSerializer(serializers.ModelSerializer):
    route = RouteOptionSerializer(read_only=True)
    drop_off_location = DropOffLocationSerializer(read_only=True)

    class Meta:
        model = ShipmentSchedule
        fields = (
            'id', 'route', 'title', 'drop_off_location', 'latest_dropoff_at',
            'departure_date', 'estimated_arrival_date', 'notes',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not is_admin_request(self):
            data['title'] = translate_database_value(data.get('title', '') or '')
            data['notes'] = translate_database_value(data.get('notes', '') or '')
        return data


class AdminShipmentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentSchedule
        fields = (
            'id', 'route', 'title', 'drop_off_location', 'latest_dropoff_at',
            'departure_date', 'estimated_arrival_date', 'notes', 'active', 'sort_order',
            'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, attrs):
        latest_dropoff = attrs.get('latest_dropoff_at', getattr(self.instance, 'latest_dropoff_at', None))
        departure = attrs.get('departure_date', getattr(self.instance, 'departure_date', None))
        arrival = attrs.get('estimated_arrival_date', getattr(self.instance, 'estimated_arrival_date', None))
        if arrival and departure and arrival < departure:
            raise serializers.ValidationError({'estimated_arrival_date': _('Estimated arrival cannot be before departure.')})
        if latest_dropoff and departure and latest_dropoff.date() > departure:
            raise serializers.ValidationError({'latest_dropoff_at': _('Latest drop-off cannot be after departure.')})
        return attrs
