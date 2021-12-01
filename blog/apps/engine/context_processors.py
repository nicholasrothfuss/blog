from collections import namedtuple
from django.urls import reverse
from .models import Category, Post


MonthLink = namedtuple('MonthLink', ['url', 'date_obj'])


def archive_links(request):
    """Provides context for generating sidebar archive links."""
    return {
        'all_categories': Category.objects.has_published_posts(),
        'all_months': [
            MonthLink(
                url=reverse('month_archive', kwargs={
                    'year': month.strftime('%Y'),
                    'month': month.strftime('%m'),
                }),
                date_obj=month,
            ) for month in Post.objects.published_months()
        ],
    }