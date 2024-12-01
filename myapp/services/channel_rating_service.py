from django.db.models import Avg, Q, FloatField, QuerySet
from django.db.models.functions import Coalesce

from myapp.models import Channel


def calculate_channel_ratings() -> QuerySet[Channel]:
    """
    Calculate ratings for channels with contents.

    Returns:
    - A queryset of channels with their average ratings, 
      sorted from highest to lowest
    """
    return Channel.objects.annotate(
        avg_rating=Coalesce(
            Avg('contents__rating', output_field=FloatField()),
            0.0
        )
    ).filter(
        Q(contents__isnull=False)
    ).distinct().order_by('-avg_rating')
