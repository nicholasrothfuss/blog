from datetime import timedelta
from django.utils import timezone


ONE_DAY_AGO = timezone.now() - timedelta(days=1)


def assert_is_now(dt):
    assert 0 <= (timezone.now() - dt).seconds < 1
