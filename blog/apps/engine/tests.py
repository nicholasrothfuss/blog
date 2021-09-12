from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from model_bakery import baker
import pytest
from pytest_django.asserts import assertTemplateUsed
from .models import Category, Post


_ONE_DAY_AGO = timezone.now() - timedelta(days=1)


@pytest.fixture
def author():
    return baker.make(User)


@pytest.fixture
def post_factory(author):
    class _Factory:
        def __init__(self, author):
            self._author = author
        def create(self, **kwargs):
            kwargs.setdefault('status', Post.Status.PUBLISHED)
            kwargs.setdefault('published_at', _ONE_DAY_AGO)
            return baker.make(Post, author=self._author, **kwargs)
    return _Factory(author)


def _create_then_fetch(model_cls, **kwargs):
    obj = baker.make(model_cls, **kwargs)
    return model_cls.objects.get(pk=obj.pk)


def _assert_is_now(dt):
    assert 0 <= (timezone.now() - dt).seconds < 1


#-----------------#
#-- View tests -- #
#-----------------#

@pytest.mark.django_db
def test_home_view(client):
    response = client.get('/')
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')


@pytest.mark.django_db
def test_permalink_view(client, post_factory):
    post = post_factory.create(status=Post.Status.PUBLISHED, published_at=_ONE_DAY_AGO)
    response = client.get(post.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'permalink.html')


@pytest.mark.django_db
def test_category_archive_view(client, post_factory):
    category = baker.make(Category)
    post = post_factory.create(categories=[category])
    response = client.get(category.get_absolute_url())
    assert response.status_code == 200
    assertTemplateUsed(response, 'category_archive.html')


#-----------------#
#-- Model tests --#
#-----------------#

#-- Post field options --#

@pytest.mark.django_db
def test_updated_at_auto_now(author):
    post = baker.prepare(Post, author=author, updated_at=_ONE_DAY_AGO)
    post.save()
    _assert_is_now(post.updated_at)


#-- Post.__str__ --#

def test_str():
    title = 'A rather dull title, dude'
    post = Post(title=title)
    assert str(post) == title


#-- Post.is_draft --#

@pytest.mark.parametrize('status,expected',
    [
        (Post.Status.DRAFT, True),
        (Post.Status.PUBLISHED, False),
        (Post.Status.HIDDEN, False),
    ]
)
def test_is_draft(status, expected):
    post = Post(status=status)
    assert post.is_draft is expected


#-- Post.is_published --#

@pytest.mark.parametrize('status,expected',
    [
        (Post.Status.DRAFT, False),
        (Post.Status.PUBLISHED, True),
        (Post.Status.HIDDEN, False),
    ]
)
def test_is_published(status, expected):
    post = Post(status=status)
    assert post.is_published is expected


#-- Post.save --#

@pytest.mark.django_db
def test_save__new_post__publish_immediately(author):
    post = baker.prepare(Post, author=author, status=Post.Status.PUBLISHED, published_at=None)
    post.save()
    _assert_is_now(post.published_at)


@pytest.mark.django_db
def test_save__new_post__draft(author):
    post = baker.prepare(Post, author=author, status=Post.Status.DRAFT, published_at=None)
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__new_post__hidden(author):
    post = baker.prepare(Post, author=author, status=Post.Status.HIDDEN, published_at=None)
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__publish_ex_draft(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.DRAFT, published_at=None)
    post.status = Post.Status.PUBLISHED
    post.save()
    _assert_is_now(post.published_at)


@pytest.mark.django_db
def test_save__update__hide_ex_draft(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.DRAFT, published_at=_ONE_DAY_AGO)
    post.status = Post.Status.HIDDEN
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__unpublish(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.PUBLISHED, published_at=_ONE_DAY_AGO)
    post.status = Post.Status.DRAFT
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__hide(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.PUBLISHED, published_at=_ONE_DAY_AGO)
    post.status = Post.Status.HIDDEN
    post.save()
    assert post.published_at == _ONE_DAY_AGO


@pytest.mark.django_db
def test_save__update__unhide(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.HIDDEN, published_at=_ONE_DAY_AGO)
    post.status = Post.Status.PUBLISHED
    post.save()
    assert post.published_at == _ONE_DAY_AGO


@pytest.mark.django_db
def test_save__update__make_draft_ex_hidden(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.HIDDEN, published_at=_ONE_DAY_AGO)
    post.status = Post.Status.DRAFT
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__keep_draft(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.DRAFT, published_at=None)
    post.title = 'New, improved title'
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__keep_published(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.PUBLISHED, published_at=_ONE_DAY_AGO)
    post.title = 'New, improved title'
    post.save()
    assert post.published_at == _ONE_DAY_AGO


@pytest.mark.django_db
def test_save__update__keep_hidden(author):
    post = _create_then_fetch(Post, author=author, status=Post.Status.HIDDEN, published_at=_ONE_DAY_AGO)
    post.title = 'New, improved title'
    post.save()
    assert post.published_at == _ONE_DAY_AGO

