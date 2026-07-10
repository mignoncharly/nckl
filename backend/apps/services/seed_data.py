from .models import ServiceType, RouteOption, AcceptedItemCategory


def create_services():
    services = [
        {'name': 'Parcel shipping', 'description': 'Parcel shipping between Germany or Europe and Cameroon.', 'icon': 'package', 'sort_order': 1},
        {'name': 'Shopping assistance', 'description': 'Shopping assistance in Douala and Bamenda.', 'icon': 'shopping-cart', 'sort_order': 2},
        {'name': 'Europe shopping delivery', 'description': 'NCKL buys products in Europe and delivers them to Cameroon after confirmation.', 'icon': 'shopping-bag', 'sort_order': 3},
        {'name': 'Travel agency pickup', 'description': 'Package pickup from travel agencies in Douala.', 'icon': 'map-pin', 'sort_order': 4},
    ]
    for data in services:
        ServiceType.objects.update_or_create(name=data['name'], defaults=data)

    routes = [
        {'name': 'Germany/Europe to Cameroon', 'direction': RouteOption.Direction.GERMANY_TO_CAMEROON, 'origin_label': 'Germany or Europe', 'destination_label': 'Cameroon', 'transit_time_display': '3 - 10 days', 'shopping_assistance_available': True, 'sort_order': 1},
        {'name': 'Cameroon to Germany/Europe', 'direction': RouteOption.Direction.CAMEROON_TO_GERMANY, 'origin_label': 'Cameroon', 'destination_label': 'Germany or Europe', 'transit_time_display': '3 - 10 days', 'shopping_assistance_available': False, 'sort_order': 2},
    ]
    for data in routes:
        RouteOption.objects.update_or_create(
            direction=data['direction'], origin_label=data['origin_label'], destination_label=data['destination_label'], defaults=data
        )

    items = [
        {'name': 'Foodstuff (dry)', 'sort_order': 1},
        {'name': 'Frozen food', 'sort_order': 2},
        {'name': 'Clothes', 'sort_order': 3},
        {'name': 'Jewelries', 'sort_order': 4},
        {'name': 'Bags', 'sort_order': 5},
        {'name': 'Shoes', 'sort_order': 6},
        {'name': 'Cosmetics', 'sort_order': 7},
        {'name': 'Hair extensions', 'sort_order': 8},
        {'name': 'Dry herbs', 'sort_order': 9},
        {'name': 'Documents', 'sort_order': 10},
        {'name': 'Phones without battery', 'requires_battery_removed': True, 'route_restriction': RouteOption.Direction.GERMANY_TO_CAMEROON, 'sort_order': 11},
        {'name': 'Small household equipment', 'max_weight_kg': 31, 'sort_order': 12},
    ]
    for data in items:
        AcceptedItemCategory.objects.update_or_create(name=data['name'], defaults=data)
