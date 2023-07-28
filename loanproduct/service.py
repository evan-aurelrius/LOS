from datetime import datetime, timedelta

from django.db.models import CharField, Q
from django.db.models.functions import Cast, TruncMinute
from ninja.errors import HttpError


def get_filtered_objects(model, query, dateformat, **kwargs):
    try:
        if kwargs.get('create_date_start'):
            create_date_start = datetime.strptime(kwargs.pop('create_date_start'), dateformat)
            query &= Q(create_date__gte=create_date_start)
        if kwargs.get('create_date_end'):
            create_date_end = datetime.strptime(kwargs.pop('create_date_end'), dateformat) + timedelta(days=1)
            query &= Q(create_date__lte=create_date_end)
        if kwargs.get('update_date_start'):
            update_date_start = datetime.strptime(kwargs.pop('update_date_start'), dateformat)
            query &= Q(update_date__gte=update_date_start)
        if kwargs.get('update_date_end'):
            update_date_end = datetime.strptime(kwargs.pop('update_date_end'), dateformat) + timedelta(days=1)
            query &= Q(update_date__lte=update_date_end)
    except ValueError:
        raise HttpError(400, "Invalid date format. Use YYYY-MM-DD.")
    for key, value in kwargs.items():
        if value:
            query &= Q(**{key + '__icontains': value})
    objects = model.objects.filter(query).annotate(
        created_date=Cast(TruncMinute("create_date"), CharField()),
        updated_date=Cast(TruncMinute("update_date"), CharField())
    )
    return objects
