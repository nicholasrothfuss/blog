from django.db import IntegrityError
import pytest
from ...models import Category
from model_bakery import baker

#------------------------------#
#-- Class-level declarations --#
#------------------------------#

#-- Field options --#

@pytest.mark.django_db
def test_name_unique():
    baker.make(Category, name='Hiking', slug='hiking1')
    cat = baker.prepare(Category, name='Hiking', slug='hiking2')
    with pytest.raises(IntegrityError):
        cat.save()


@pytest.mark.django_db
def test_slug_unique():
    baker.make(Category, name='Hiking1', slug='hiking')
    cat = baker.prepare(Category, name='Hiking2', slug='hiking')
    with pytest.raises(IntegrityError):
        cat.save()


#-- Meta options --#

@pytest.mark.django_db
def test_default_ordering():
    c1 = baker.make(Category, name='Hiking')
    c2 = baker.make(Category, name='Baseball')
    c3 = baker.make(Category, name='Waterfalls')
    c4 = baker.make(Category, name='Politics')
    c5 = baker.make(Category, name='Music')

    assert list(Category.objects.all()) == [c2, c1, c5, c4, c3]


#--------------------------------------------#
#-- Standard Django instance model methods --#
#--------------------------------------------#

#-- __str__ --#

def test_str():
    name = 'A Boring Category'
    cat = Category(name=name)
    assert str(cat) == name



#-- get_absolute_url --#

def test_get_absolute_url():
    cat = Category(slug='hiking-and-travel')
    assert cat.get_absolute_url() == '/categories/hiking-and-travel/'
