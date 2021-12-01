from model_bakery import baker
import pytest
from pytest_django.asserts import assertTemplateUsed

from ..utils import (
    assert_contains_post_title, 
    assert_contains_post_permalinks,
    assert_not_contains_post_categories, 
    tz_datetime
)
from ...models import Category


#-- Tests for conditions where an unpaginated 200 response is expected --#

@pytest.mark.django_db
def test_single_published_post_with_one_category(client, post_factory):
    category = baker.make(Category, name='Python')
    post = post_factory.create(
        title='Using Django', 
        slug='using-django',
        categories=[category], 
        published_at=tz_datetime(2021, 6, 5)
    )
    response = client.get(category.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'category_archive.html')

    assert_contains_post_title(response, 'Using Django')
    assert_contains_post_permalinks(response, post.get_absolute_url())
    assert_not_contains_post_categories(response)


@pytest.mark.django_db
def test_multiple_published_posts_with_one_category(client, post_factory):
    category = baker.make(Category)
    p1 = post_factory.create(categories=[category], published_at=tz_datetime(2021, 6, 5))
    p2 = post_factory.create(categories=[category], published_at=tz_datetime(2021, 7, 10, 11))
    p3 = post_factory.create(categories=[category], published_at=tz_datetime(2021, 4, 3))
    p4 = post_factory.create(categories=[category], published_at=tz_datetime(2021, 7, 10, 5))
    response = client.get(category.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'category_archive.html')
    assert response.context['category'] == category
    assert list(response.context['posts']) == [p2, p4, p1, p3]


@pytest.mark.django_db
def test_multiple_published_posts_spread_across_categories(client, post_factory):
    c1 = baker.make(Category)
    c2 = baker.make(Category)
    post_factory.create(categories=[c1], published_at=tz_datetime(2021, 6, 5))
    p2 = post_factory.create(categories=[c2], published_at=tz_datetime(2021, 7, 10, 11))
    p3 = post_factory.create(categories=[c2], published_at=tz_datetime(2021, 4, 3))
    p4 = post_factory.create(categories=[c2], published_at=tz_datetime(2021, 7, 10, 5))
    response = client.get(c2.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'category_archive.html')
    assert response.context['category'] == c2
    assert list(response.context['posts']) == [p2, p4, p3]


@pytest.mark.django_db
def test_multiple_published_posts_with_multiple_categories(client, post_factory):
    c1 = baker.make(Category)
    c2 = baker.make(Category)
    baker.make(Category)
    post_factory.create(categories=[c1], published_at=tz_datetime(2021, 6, 5))
    p2 = post_factory.create(categories=[c1, c2], published_at=tz_datetime(2021, 7, 10, 11))
    p3 = post_factory.create(categories=[c2], published_at=tz_datetime(2021, 4, 3))
    p4 = post_factory.create(categories=[c1, c2], published_at=tz_datetime(2021, 7, 10, 5))
    response = client.get(c2.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'category_archive.html')
    assert response.context['category'] == c2
    assert list(response.context['posts']) == [p2, p4, p3]


#-- Tests for conditions where a 404 response is expected --#

@pytest.mark.django_db
def test_category_has_no_posts(client, post_factory):
    c1 = baker.make(Category)
    c2 = baker.make(Category)
    c3 = baker.make(Category)
    post_factory.create(categories=[c1], published_at=tz_datetime(2021, 6, 5))
    post_factory.create(categories=[c1, c2], published_at=tz_datetime(2021, 7, 10, 11))
    post_factory.create(categories=[c2], published_at=tz_datetime(2021, 4, 3))
    post_factory.create(categories=[c1, c2], published_at=tz_datetime(2021, 7, 10, 5))
    response = client.get(c3.get_absolute_url())
    assert response.status_code == 404


@pytest.mark.django_db
def test_category_only_has_draft(client, post_factory):
    c1 = baker.make(Category)
    c2 = baker.make(Category)
    c3 = baker.make(Category)
    post_factory.create(categories=[c1], published_at=tz_datetime(2021, 6, 5))
    post_factory.create(categories=[c1, c2], published_at=tz_datetime(2021, 7, 10, 11))
    post_factory.create(categories=[c2], published_at=tz_datetime(2021, 4, 3))
    post_factory.create_draft(categories=[c3])
    response = client.get(c3.get_absolute_url())
    assert response.status_code == 404


@pytest.mark.django_db
def test_category_only_has_hidden_post(client, post_factory):
    c1 = baker.make(Category)
    c2 = baker.make(Category)
    c3 = baker.make(Category)
    post_factory.create(categories=[c1], published_at=tz_datetime(2021, 6, 5))
    post_factory.create(categories=[c1, c2], published_at=tz_datetime(2021, 7, 10, 11))
    post_factory.create(categories=[c2], published_at=tz_datetime(2021, 4, 3))
    post_factory.create_hidden(categories=[c3], published_at=tz_datetime(2021, 7, 10, 5))
    response = client.get(c3.get_absolute_url())
    assert response.status_code == 404