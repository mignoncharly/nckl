from django.utils.translation import gettext, gettext_noop


# Database-backed catalog values shipped by the seed data. gettext_noop keeps
# them extractable while translation happens only when a response is rendered.
DATABASE_MESSAGES = (
    gettext_noop('Parcel shipping'),
    gettext_noop('Shopping assistance'),
    gettext_noop('Europe shopping delivery'),
    gettext_noop('Travel agency pickup'),
    gettext_noop('Germany/Europe to Cameroon'),
    gettext_noop('Cameroon to Germany/Europe'),
    gettext_noop('Foodstuff (dry)'),
    gettext_noop('Frozen food'),
    gettext_noop('Clothes'),
    gettext_noop('Jewelries'),
    gettext_noop('Bags'),
    gettext_noop('Shoes'),
    gettext_noop('Cosmetics'),
    gettext_noop('Hair extensions'),
    gettext_noop('Dry herbs'),
    gettext_noop('Documents'),
    gettext_noop('Phones without battery'),
    gettext_noop('Small household equipment'),
    gettext_noop('Cameroon'),
    gettext_noop('Germany'),
    gettext_noop('Europe'),
    gettext_noop('Douala'),
    gettext_noop('Bamenda'),
    gettext_noop('Berlin'),
    gettext_noop('Leipzig'),
    gettext_noop('Departure date'),
)


def translate_database_value(value):
    return gettext(value) if value else value


def is_admin_request(serializer):
    request = serializer.context.get('request')
    return bool(request and request.path.startswith('/api/admin/'))
