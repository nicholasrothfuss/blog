import pytest
from ..utils import tz_datetime
from ...models import Post, PostQuerySet


#-- published() --#

@pytest.mark.django_db
def test_published_one_published(post_factory):
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5, 13))
    post_factory.create_draft()
    post_factory.create_hidden()

    qs = PostQuerySet(Post)
    assert list(qs.published()) == [p1]


@pytest.mark.django_db
def test_published_multiple_published(post_factory):
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5, 13))
    p2 = post_factory.create(published_at=tz_datetime(2021, 5, 3))
    p3 = post_factory.create(published_at=tz_datetime(2021, 6, 5, 15))
    p4 = post_factory.create(published_at=tz_datetime(2021, 5, 18))
    post_factory.create_draft()
    post_factory.create_hidden()

    qs = PostQuerySet(Post)
    assert list(qs.published()) == [p3, p1, p4, p2]


@pytest.mark.django_db
def test_published_none_published(post_factory):
    post_factory.create_draft()
    post_factory.create_hidden()

    qs = PostQuerySet(Post)
    assert list(qs.published()) == []


@pytest.mark.django_db
def test_published_all_published_filtered_out(post_factory):
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5, 13))
    p2 = post_factory.create(published_at=tz_datetime(2021, 5, 3))
    p3 = post_factory.create(published_at=tz_datetime(2021, 6, 5, 15))
    p4 = post_factory.create(published_at=tz_datetime(2021, 5, 18))
    post_factory.create_draft()
    post_factory.create_hidden()

    qs = PostQuerySet(Post).filter(published_at__lt=tz_datetime(2019, 1, 1))
    assert list(qs.published()) == []