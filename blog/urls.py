from django.contrib import admin
from django.urls import path, re_path
from blog.apps.engine import views as core_views

urlpatterns = [
    re_path(
        r'^posts/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/$',
        core_views.PermalinkView.as_view(), 
        name='permalink'
    ),
    path(
        'categories/<slug:slug>/', 
        core_views.CategoryArchiveView.as_view(), 
        name='category_archive'
    ),
    path('admin/', admin.site.urls),
    path('', core_views.HomePostListView.as_view(), name='home'),
]
