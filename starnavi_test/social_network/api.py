from django.contrib.contenttypes.models import (
    ContentType,
)
from django.db.models import (
    Count,
    DateField,
)
from django.db.models.functions import (
    TruncDay,
)

from .models import (
    Like,
    UserProfile,
)


def get_obj_type(obj):
    return ContentType.objects.get_for_model(obj)


def add_like(obj, user):
    Like.objects.get_or_create(
        content_type=get_obj_type(obj),
        object_id=obj.id,
        user=user,
    )


def remove_like(obj, user):
    Like.objects.filter(
        content_type=get_obj_type(obj),
        object_id=obj.id,
        user__user=user,
    ).delete()


def get_count_likes_by_date(date_from, date_to):
    return Like.objects.filter(
        date__range=(date_from, date_to),
    ).annotate(
        day=TruncDay(
            'date',
            output_field=DateField(),
        ),
    ).values(
        'day',
    ).annotate(
        count=Count('id'),
    )


def get_user_activity(user_id):
    if user_id is not None:
        return UserProfile.objects.filter(
            id=user_id,
        ).first()
