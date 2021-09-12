from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from model_bakery import baker
import pytest
from .utils import ONE_DAY_AGO
from ..models import Post


@pytest.fixture
def author():
    return baker.make(User)


@pytest.fixture
def post_factory(author):
    class _Factory:
        def __init__(self, author):
            self._author = author
        def create(self, *, _save=True, **kwargs):
            kwargs.setdefault('status', Post.Status.PUBLISHED)
            kwargs.setdefault('published_at', ONE_DAY_AGO)
            baker_f = baker.make if _save else baker.prepare
            return baker_f(Post, author=self._author, **kwargs)            
        def create_draft(self, *, _save=True, **kwargs):
            kwargs['status'] = Post.Status.DRAFT
            kwargs['published_at'] = None
            return self.create(_save=_save, **kwargs)
        def create_hidden(self, *, _save=True, **kwargs):
            kwargs['status'] = Post.Status.HIDDEN
            return self.create(_save=_save, **kwargs)
    return _Factory(author)