import pytest
from ..utils import assert_is_now, tz_datetime, ONE_DAY_AGO
from ...models import Post


#-- Field options --#

def test_status_default():
    assert Post().status == Post.Status.DRAFT
    

@pytest.mark.django_db
def test_updated_at_auto_now(post_factory):
    post = post_factory.create(updated_at=ONE_DAY_AGO)
    post.save()
    assert_is_now(post.updated_at)


#-- Meta options --#

@pytest.mark.django_db
def test_default_ordering(post_factory):
    p1 = post_factory.create(published_at=tz_datetime(2021, 6, 5, 13))
    p2 = post_factory.create(published_at=tz_datetime(2021, 5, 3))
    p3 = post_factory.create(published_at=tz_datetime(2021, 6, 5, 15))
    p4 = post_factory.create(published_at=tz_datetime(2021, 5, 18))

    assert list(Post.objects.all()) == [p3, p1, p4, p2]


#-- __str__() --#

def test_str():
    title = 'A rather dull title, dude'
    post = Post(title=title)
    assert str(post) == title


#-- get_absolute_url() --#

def test_get_absolute_url_published():
    post = Post(
        status=Post.Status.PUBLISHED, 
        slug='foo-bar', 
        published_at=tz_datetime(2020, 6, 5, 13)
    )
    assert post.get_absolute_url() == '/2020/06/foo-bar/'


#-- is_draft --#

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


#-- is_published --#

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


#-- save() --#

@pytest.mark.django_db
def test_save__new_post__publish_immediately(post_factory):
    post = post_factory.create(published_at=None, _save=False)
    post.save()
    assert_is_now(post.published_at)


@pytest.mark.django_db
def test_save__new_post__draft(post_factory):
    post = post_factory.create_draft(_save=False)
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__new_post__hidden(post_factory):
    post = post_factory.create_hidden(published_at=None, _save=False)
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__publish_ex_draft(post_factory):
    post = post_factory.create_draft()
    post.status = Post.Status.PUBLISHED
    post.save()
    assert_is_now(post.published_at)


@pytest.mark.django_db
def test_save__update__hide_ex_draft(post_factory):
    post = post_factory.create_draft()
    post.status = Post.Status.HIDDEN
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__unpublish(post_factory):
    post = post_factory.create()
    post.status = Post.Status.DRAFT
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__hide(post_factory):
    post = post_factory.create()
    post.status = Post.Status.HIDDEN
    post.save()
    assert post.published_at == ONE_DAY_AGO


@pytest.mark.django_db
def test_save__update__unhide(post_factory):
    post = post_factory.create_hidden()
    post.status = Post.Status.PUBLISHED
    post.save()
    assert post.published_at == ONE_DAY_AGO


@pytest.mark.django_db
def test_save__update__make_draft_ex_hidden(post_factory):
    post = post_factory.create_hidden()
    post.status = Post.Status.DRAFT
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__keep_draft(post_factory):
    post = post_factory.create_draft()
    post.title = 'New, improved title'
    post.save()
    assert post.published_at is None


@pytest.mark.django_db
def test_save__update__keep_published(post_factory):
    post = post_factory.create()
    post.title = 'New, improved title'
    post.save()
    assert post.published_at == ONE_DAY_AGO


@pytest.mark.django_db
def test_save__update__keep_hidden(post_factory):
    post = post_factory.create_hidden()
    post.title = 'New, improved title'
    post.save()
    assert post.published_at == ONE_DAY_AGO