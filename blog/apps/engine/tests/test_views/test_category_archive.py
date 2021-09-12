from model_bakery import baker
import pytest
from pytest_django.asserts import assertTemplateUsed
from ...models import Category


@pytest.mark.django_db
def test_category_archive_view(client, post_factory):
    category = baker.make(Category)
    post = post_factory.create(categories=[category])
    response = client.get(category.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'category_archive.html')