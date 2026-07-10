from datetime import date, datetime, time
from django.utils import timezone
from .models import DropOffLocation, ShipmentSchedule, LoadingDate
from apps.services.models import RouteOption


def create_schedules():
    locations = [
        {'name': 'Bamenda - Shed A7', 'city': 'Bamenda', 'country': 'Cameroon', 'address': 'Commercial avenue entrance to the stadium, Shed A7', 'phone': '+237 674574041 / +237 622441020', 'opening_hours': 'Tuesday - Saturday, 11am - 3pm', 'sort_order': 1},
        {'name': 'Douala - Bonaberi', 'city': 'Douala', 'country': 'Cameroon', 'address': 'Rue 4.670, Bonaberi, 4 Etages, near Carrefour Bamoutos, before Jehovah Witness Hall, Douala, Littoral, Cameroon', 'phone': '+237 675745056', 'whatsapp': '+237 675745056', 'sort_order': 2},
        {'name': 'Douala - Nouvelle route Bonaberi', 'city': 'Douala', 'country': 'Cameroon', 'address': 'A la nouvelle route Bonaberi, Dola service station', 'phone': '+237 674972802', 'sort_order': 3},
        {'name': 'Berlin', 'city': 'Berlin', 'country': 'Germany', 'address': 'Eichushallee 53 Apartment 227, 12437 Berlin', 'whatsapp': '+49 15222376184', 'details': 'WhatsApp only', 'sort_order': 4},
        {'name': 'Leipzig - Ariana Mark Leipzig', 'city': 'Leipzig', 'country': 'Germany', 'address': 'Rosa-Luxemburg Strasse 10, 04103 Leipzig', 'phone': '+49 15773620710', 'sort_order': 5},
    ]
    for data in locations:
        DropOffLocation.objects.update_or_create(name=data['name'], city=data['city'], defaults=data)

    route = RouteOption.objects.filter(direction=RouteOption.Direction.CAMEROON_TO_GERMANY).first()
    douala = DropOffLocation.objects.filter(city='Douala').order_by('sort_order').first()
    if route and douala:
        ShipmentSchedule.objects.get_or_create(
            route=route,
            title='July 2026 Cameroon to Germany/Europe shipment',
            defaults={
                'drop_off_location': douala,
                'latest_dropoff_at': timezone.make_aware(datetime.combine(date(2026, 7, 11), time(17, 0))),
                'departure_date': date(2026, 7, 12),
                'estimated_arrival_date': date(2026, 7, 16),
                'notes': 'Visible flyer schedule. Confirm whether this is one-time or recurring before production use.',
            },
        )
    LoadingDate.objects.get_or_create(
        date=date(2026, 7, 12),
        defaults={'title': 'Departure date', 'description': 'Visible NCKL flyer departure date for Cameroon to Germany/Europe'}
    )
