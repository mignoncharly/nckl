from django.db import models
from django.utils.translation import gettext_lazy as _


class PickupRegion(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, default='Allemagne')
    cities = models.TextField(help_text=_("Comma-separated list of cities"))
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PickupSchedule(models.Model):
    region = models.ForeignKey(PickupRegion, on_delete=models.CASCADE, related_name='schedules')
    title = models.CharField(max_length=255, blank=True)
    cities = models.TextField(blank=True, help_text=_("Override cities for this schedule"))
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.region.name} - {self.start_date}"


class LoadingDate(models.Model):
    date = models.DateField(unique=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return _("Loading %(date)s") % {'date': self.date}


class DropOffLocation(models.Model):
    class LocationType(models.TextChoices):
        DROP_OFF = 'drop_off', _('Drop-off')
        PICKUP = 'pickup', _('Pickup')
        BOTH = 'both', _('Drop-off and pickup')

    name = models.CharField(max_length=160)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    location_type = models.CharField(max_length=20, choices=LocationType.choices, default=LocationType.DROP_OFF)
    address = models.TextField(blank=True)
    details = models.TextField(blank=True)
    phone = models.CharField(max_length=80, blank=True)
    whatsapp = models.CharField(max_length=80, blank=True)
    opening_hours = models.CharField(max_length=180, blank=True)
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'country', 'city', 'name']
        indexes = [
            models.Index(fields=['active', 'country', 'city']),
            models.Index(fields=['location_type', 'active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city}"


class ShipmentSchedule(models.Model):
    route = models.ForeignKey('services.RouteOption', on_delete=models.SET_NULL, null=True, blank=True, related_name='shipment_schedules')
    title = models.CharField(max_length=180, blank=True)
    drop_off_location = models.ForeignKey(DropOffLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipment_schedules')
    latest_dropoff_at = models.DateTimeField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    estimated_arrival_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['latest_dropoff_at', 'departure_date', 'sort_order']
        indexes = [
            models.Index(fields=['active', 'departure_date']),
            models.Index(fields=['active', 'latest_dropoff_at']),
        ]

    def __str__(self):
        label = self.title or (self.route.name if self.route else _('Shipment schedule'))
        return f"{label} - {self.departure_date or self.latest_dropoff_at or ''}"
