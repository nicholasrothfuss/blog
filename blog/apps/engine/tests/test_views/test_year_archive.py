import datetime
from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed
from ..utils import tz_datetime


def _get_year_archive_url(post=None, *, force_year=None):
    ref_date = post.published_at if force_year is None else force_year
    return reverse('year_archive', kwargs={'year': ref_date.strftime('%Y')})


#-- Tests for conditions where an unpaginated 200 response is expected --#

@pytest.mark.django_db
def test_single_published_post(client, post_factory):
    """The post should be in the response."""
    post = post_factory.create()
    response = client.get(_get_year_archive_url(post))
    assert response.status_code == 200
    assertTemplateUsed(response, 'year_archive.html')
    assert [post] == list(response.context['posts'])


@pytest.mark.django_db
def test_multiple_published_posts_same_year(client, post_factory):
    """All posts should be in the response."""
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5))
    p2 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 12))
    p3 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 13))
    p4 = post_factory.create(published_at=tz_datetime(2021, 6, 8))
    response = client.get(_get_year_archive_url(p4))
    assert response.status_code == 200
    assertTemplateUsed(response, 'year_archive.html')
    assert [p4, p1, p3, p2] == list(response.context['posts'])


@pytest.mark.django_db
def test_multiple_published_posts_different_years(client, post_factory):
    """The post from the other year should be excluded from the response."""
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5))
    p2 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 12))
    p3 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 13))
    post_factory.create(published_at=tz_datetime(2020, 7, 3))
    response = client.get(_get_year_archive_url(p3))
    assert response.status_code == 200
    assertTemplateUsed(response, 'year_archive.html')
    assert [p1, p3, p2] == list(response.context['posts'])


@pytest.mark.django_db
def test_draft_post_exists(client, post_factory):
    """The draft should be excluded from the response."""
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5))
    p2 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 12))
    p3 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 13))
    post_factory.create_draft()
    response = client.get(_get_year_archive_url(p3))
    assert response.status_code == 200
    assertTemplateUsed(response, 'year_archive.html')
    assert [p1, p3, p2] == list(response.context['posts'])

@pytest.mark.django_db
def test_year_has_hidden_post(client, post_factory):
    """The hidden post should be excluded from the response."""
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5))
    p2 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 12))
    p3 = post_factory.create(published_at=tz_datetime(2021, 6, 4, 13))
    post_factory.create_hidden(published_at=tz_datetime(2021, 6, 8))
    response = client.get(_get_year_archive_url(p3))
    assert response.status_code == 200
    assertTemplateUsed(response, 'year_archive.html')
    assert [p1, p3, p2] == list(response.context['posts'])


#-- Tests for conditions where a 404 response is expected --#

@pytest.mark.django_db
def test_year_has_no_posts(client, post_factory):
    post_factory.create(published_at=tz_datetime(2021, 6, 5))
    post_factory.create(published_at=tz_datetime(2021, 6, 4, 12))
    response = client.get(_get_year_archive_url(force_year=datetime.date(2020, 6, 1)))
    assert response.status_code == 404


@pytest.mark.django_db
def test_year_only_has_hidden_post(client, post_factory):
    p1 = post_factory.create_hidden(published_at=tz_datetime(2021, 6, 5))
    post_factory.create(published_at=tz_datetime(2020, 7, 3))
    response = client.get(_get_year_archive_url(p1))
    assert response.status_code == 404