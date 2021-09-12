import pytest
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_permalink_view(client, post_factory):
    post = post_factory.create()
    response = client.get(post.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'permalink.html')
