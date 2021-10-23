import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_published_post(client, post_factory):
    post = post_factory.create()
    response = client.get(post.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'permalink.html')


@pytest.mark.django_db
def test_hidden_post(client, post_factory):
    """For now a 404 response should be returned if the post is hidden.
    
    In the future, finer-grained responses incorporating why the post
    was hidden may be desirable.

    """
    post = post_factory.create_hidden()
    response = client.get(post.get_absolute_url())
    assert response.status_code == 404