from datetime import date

import pytest
from model_bakery import baker

from ..context_processors import archive_links
from ..models import Category
from .utils import tz_datetime


@pytest.mark.django_db
def test_archive_links(post_factory):
    """Tests the archive_links context_processor under common production conditions.
    
    Specifically, this verifies:
        * Categories are returned in ascending order by name.
        * Months are returned in descending order.
        * Duplicate categories or months are not returned.
        * Categories only associated with draft or hidden posts are not returned.
        * Months only associated with hidden posts are not returned.
        * The mere fact a category or month is associated with draft and/or hidden 
            post does not preclude it from being returned.

    """
    c1 = baker.make(Category, name='Hiking')
    c2 = baker.make(Category, name='Python')
    c3 = baker.make(Category, name='Baseball')
    c4 = baker.make(Category, name='Nothing Useful')
    c5 = baker.make(Category, name='Also Nothing')

    post_factory.create(published_at=tz_datetime(2020, 6, 5, 13), categories=[c1, c2])
    post_factory.create(published_at=tz_datetime(2021, 5, 3), categories=[c1, c3])
    post_factory.create(published_at=tz_datetime(2021, 8, 5, 15))
    post_factory.create(published_at=tz_datetime(2021, 5, 18))
    post_factory.create_draft(categories=[c1, c4])
    post_factory.create_hidden(published_at=tz_datetime(2020, 9, 6), categories=[c2, c5])
    post_factory.create_hidden(published_at=tz_datetime(2021, 8, 13))

    # No need to stub a request object as the function shouldn't use that argument.
    ctx = archive_links(None)

    assert list(ctx['all_categories']) == [c3, c1, c2]
    assert [m.date_obj for m in ctx['all_months']] == \
        [date(2021, 8, 1), date(2021, 5, 1), date(2020, 6, 1)]
    assert [m.url for m in ctx['all_months']] == \
        ['/2021/08/', '/2021/05/', '/2020/06/']
