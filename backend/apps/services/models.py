from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text=_("Icon identifier for frontend"))
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class RouteOption(models.Model):
    class Direction(models.TextChoices):
        GERMANY_TO_CAMEROON = 'germany_cameroon', _('Germany or Europe to Cameroon')
        CAMEROON_TO_GERMANY = 'cameroon_germany', _('Cameroon to Germany or Europe')

    name = models.CharField(max_length=160)
    direction = models.CharField(max_length=40, choices=Direction.choices)
    origin_label = models.CharField(max_length=120)
    destination_label = models.CharField(max_length=120)
    transit_time_display = models.CharField(
        max_length=120,
        blank=True,
        help_text=_('Customer-facing wording, e.g. "3 - 10 days". Keep configurable because source materials conflict.'),
    )
    shopping_assistance_available = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['active', 'direction']),
            models.Index(fields=['sort_order']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['direction', 'origin_label', 'destination_label'], name='unique_route_direction_origin_destination'),
        ]

    def __str__(self):
        return self.name


class AcceptedItemCategory(models.Model):
    class RouteRestriction(models.TextChoices):
        NONE = '', _('No route restriction')
        GERMANY_TO_CAMEROON = RouteOption.Direction.GERMANY_TO_CAMEROON, _('Germany or Europe to Cameroon only')
        CAMEROON_TO_GERMANY = RouteOption.Direction.CAMEROON_TO_GERMANY, _('Cameroon to Germany or Europe only')

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    max_weight_kg = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    requires_battery_removed = models.BooleanField(default=False)
    route_restriction = models.CharField(max_length=40, choices=RouteRestriction.choices, blank=True, default='')
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['active', 'sort_order']),
            models.Index(fields=['route_restriction']),
        ]

    def __str__(self):
        return self.name
