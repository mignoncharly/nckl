from django.db import models
from django.conf import settings
from apps.customers.models import Customer
from apps.services.models import ServiceType, RouteOption, AcceptedItemCategory
from apps.destinations.models import DestinationCity
from apps.schedules.models import DropOffLocation, ShipmentSchedule
from django.utils.translation import gettext_lazy as _

class TransportRequest(models.Model):
    STATUS_CHOICES = [
        ('new', _('New')),
        ('contacted', _('Contacted')),
        ('confirmed', _('Confirmed')),
        ('pickup_scheduled', _('Pickup scheduled')),
        ('received', _('Received')),
        ('loaded', _('Loaded')),
        ('in_transit', _('In transit')),
        ('arrived_cameroon', _('Arrived in Cameroon')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', _('Unpaid')),
        ('partial', _('Partially paid')),
        ('paid', _('Paid')),
        ('refunded', _('Refunded')),
    ]
    reference_code = models.CharField(max_length=50, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requests')
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, blank=True)
    route_option = models.ForeignKey(RouteOption, on_delete=models.SET_NULL, null=True, blank=True, related_name='transport_requests')
    accepted_item = models.ForeignKey(AcceptedItemCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='transport_requests')
    drop_off_location = models.ForeignKey(DropOffLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='transport_requests')
    shipment_schedule = models.ForeignKey(ShipmentSchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='transport_requests')
    pickup_city = models.CharField(max_length=200)
    pickup_address = models.TextField()
    preferred_pickup_date = models.DateField(null=True, blank=True)
    destination_city = models.ForeignKey(DestinationCity, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    dimensions = models.CharField(max_length=200, blank=True)
    estimated_weight = models.CharField(max_length=100, blank=True)
    item_weight_kg = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    phones_without_battery_confirmed = models.BooleanField(default=False)
    shopping_assistance_requested = models.BooleanField(default=False)
    shopping_details = models.TextField(blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    internal_notes = models.TextField(blank=True)
    customer_notes = models.TextField(blank=True)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference_code']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['route_option', 'status']),
        ]

    def __str__(self):
        return f"{self.reference_code} - {self.customer.full_name}"

class TransportRequestPhoto(models.Model):
    request = models.ForeignKey(TransportRequest, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='request_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _("Photo %(photo_id)s for %(reference)s") % {
            'photo_id': self.id,
            'reference': self.request.reference_code,
        }


class RequestStatusEvent(models.Model):
    """One recorded status transition for a TransportRequest (customer-facing
    history; distinct from the ops-facing AuditLog)."""
    request = models.ForeignKey(
        TransportRequest, on_delete=models.CASCADE, related_name='status_events'
    )
    from_status = models.CharField(max_length=30, blank=True)
    to_status = models.CharField(max_length=30)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.request.reference_code}: {self.from_status} -> {self.to_status}"


class RequestComment(models.Model):
    """A comment on a request. is_internal=True comments are admin-only; the
    customer can read/post only non-internal ones on their own request."""
    request = models.ForeignKey(
        TransportRequest, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    body = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment on {self.request.reference_code} by {self.author}"
