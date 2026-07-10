from rest_framework import serializers
from .models import TransportRequest, TransportRequestPhoto, RequestStatusEvent, RequestComment
from apps.customers.serializers import CustomerSerializer
from apps.services.serializers import ServiceTypeSerializer, RouteOptionSerializer, AcceptedItemCategorySerializer
from apps.destinations.serializers import DestinationCitySerializer
from apps.schedules.serializers import DropOffLocationSerializer, ShipmentScheduleSerializer
from apps.uploads.validators import validate_image_extension, validate_file_size, validate_image_content
from django.utils.translation import gettext as _

class TransportRequestPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportRequestPhoto
        fields = ('id', 'image', 'uploaded_at')

class RequestStatusEventSerializer(serializers.ModelSerializer):
    actor_email = serializers.CharField(source='actor.email', read_only=True, default=None)

    class Meta:
        model = RequestStatusEvent
        fields = ('id', 'from_status', 'to_status', 'actor_email', 'note', 'created_at')
        read_only_fields = fields

class TransportRequestListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    destination_name = serializers.CharField(source='destination_city.name', read_only=True)
    route_name = serializers.CharField(source='route_option.name', read_only=True, default='')
    accepted_item_name = serializers.CharField(source='accepted_item.name', read_only=True, default='')

    class Meta:
        model = TransportRequest
        fields = ('id', 'reference_code', 'customer_name', 'pickup_city', 'destination_name', 'route_name', 'accepted_item_name', 'status', 'created_at', 'preferred_pickup_date')

class PublicTransportRequestTrackingSerializer(serializers.ModelSerializer):
    """Minimal, privacy-safe projection for anonymous tracking by reference code.

    Anyone who knows a reference code can read this, so it deliberately omits
    everything private: customer name/phone/email, the full pickup address,
    internal notes, prices, photos, and free-text description/notes. Only the
    coarse shipment progress is exposed. Keep the full
    ``TransportRequestDetailSerializer`` for admin / authenticated detail views.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    destination_name = serializers.CharField(source='destination_city.name', read_only=True)
    route_name = serializers.CharField(source='route_option.name', read_only=True, default='')

    class Meta:
        model = TransportRequest
        fields = (
            'reference_code',
            'status',
            'status_display',
            'service_type_name',
            'route_name',
            'pickup_city',
            'destination_name',
            'preferred_pickup_date',
            'created_at',
        )
        read_only_fields = fields


class CustomerTransportRequestDetailSerializer(serializers.ModelSerializer):
    """Full detail of a request for its OWNER (an authenticated customer).

    Includes the private fields the customer is entitled to see about their own
    shipment — address, prices, photos, their own notes — but NEVER the
    admin-only ``internal_notes``.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    destination_name = serializers.CharField(source='destination_city.name', read_only=True)
    route_name = serializers.CharField(source='route_option.name', read_only=True, default='')
    accepted_item_name = serializers.CharField(source='accepted_item.name', read_only=True, default='')
    drop_off_location = DropOffLocationSerializer(read_only=True)
    shipment_schedule = ShipmentScheduleSerializer(read_only=True)
    photos = TransportRequestPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = TransportRequest
        fields = (
            'reference_code', 'status', 'status_display',
            'service_type_name', 'route_name', 'accepted_item_name', 'drop_off_location', 'shipment_schedule', 'pickup_city', 'pickup_address',
            'preferred_pickup_date', 'destination_name',
            'quantity', 'dimensions', 'estimated_weight', 'item_weight_kg', 'phones_without_battery_confirmed', 'shopping_assistance_requested', 'shopping_details', 'description',
            'customer_notes', 'estimated_price', 'final_price',
            'photos', 'created_at', 'updated_at',
        )
        read_only_fields = fields


class TransportRequestDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    route_option = RouteOptionSerializer(read_only=True)
    accepted_item = AcceptedItemCategorySerializer(read_only=True)
    drop_off_location = DropOffLocationSerializer(read_only=True)
    shipment_schedule = ShipmentScheduleSerializer(read_only=True)
    destination_city = DestinationCitySerializer(read_only=True)
    photos = TransportRequestPhotoSerializer(many=True, read_only=True)
    status_events = RequestStatusEventSerializer(many=True, read_only=True)

    class Meta:
        model = TransportRequest
        fields = '__all__'

class TransportRequestCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(
        child=serializers.ImageField(
            max_length=None,
            allow_empty_file=False,
            use_url=True,
            validators=[validate_image_extension, validate_file_size, validate_image_content],
        ),
        write_only=True,
        required=False,
        max_length=10,
    )

    class Meta:
        model = TransportRequest
        fields = [
            'service_type', 'route_option', 'accepted_item', 'drop_off_location', 'shipment_schedule',
            'pickup_city', 'pickup_address', 'preferred_pickup_date', 'destination_city',
            'quantity', 'dimensions', 'estimated_weight', 'item_weight_kg',
            'phones_without_battery_confirmed', 'shopping_assistance_requested',
            'shopping_details', 'description', 'customer_notes', 'photos'
        ]


    def validate(self, attrs):
        route = attrs.get('route_option')
        item = attrs.get('accepted_item')
        weight = attrs.get('item_weight_kg')
        if item and route and item.route_restriction and item.route_restriction != route.direction:
            raise serializers.ValidationError({
                'accepted_item': _('This item category is not available for the selected route.')
            })
        if item and item.max_weight_kg is not None and weight is not None and weight > item.max_weight_kg:
            raise serializers.ValidationError({
                'item_weight_kg': _('This item category has a maximum weight of %(weight)s kg.') % {'weight': item.max_weight_kg}
            })
        if item and item.requires_battery_removed and not attrs.get('phones_without_battery_confirmed'):
            raise serializers.ValidationError({
                'phones_without_battery_confirmed': _('Confirm that phone batteries are removed for this route.')
            })
        return attrs

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(_('Quantity must be at least 1.'))
        return value

    def create(self, validated_data):
        from .reference import create_transport_request_with_reference
        photos_data = validated_data.pop('photos', [])
        # Reference code is assigned here (with collision retry), not in the view,
        # so the read-of-latest and the INSERT happen together.
        request_obj = create_transport_request_with_reference(**validated_data)
        for photo in photos_data:
            TransportRequestPhoto.objects.create(request=request_obj, image=photo)
        return request_obj

class TransportRequestStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=TransportRequest.STATUS_CHOICES)
    internal_notes = serializers.CharField(required=False, allow_blank=True)


class RequestCommentSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(source='author.email', read_only=True, default=None)

    class Meta:
        model = RequestComment
        fields = ('id', 'author_email', 'body', 'is_internal', 'created_at')
        # is_internal is set server-side per role (owner -> always False).
        read_only_fields = ('id', 'author_email', 'is_internal', 'created_at')
