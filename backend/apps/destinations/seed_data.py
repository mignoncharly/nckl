from .models import DestinationCity


def create_destinations():
    for city in ['Cameroon', 'Germany', 'Europe', 'Douala', 'Bamenda', 'Berlin', 'Leipzig']:
        DestinationCity.objects.get_or_create(name=city)
