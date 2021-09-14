from django.contrib import admin
from django.urls import path, re_path
from blog.apps.engine import views as core_views

urlpatterns = [
    re_path(
        r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$',
        core_views.PostPermalinkView.as_view(), 
        name='permalink'
    ),
    re_path(
        r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        core_views.PostMonthArchiveView.as_view(), 
        name='month_archive'
    ),
    re_path(
        r'^(?P<year>[0-9]{4})/$',
        core_views.PostYearArchiveView.as_view(), 
        name='year_archive'
    ),
    path(
        'categories/<slug:slug>/', 
        core_views.PostCategoryArchiveView.as_view(), 
        name='category_archive'
    ),
    path('admin/', admin.site.urls),
    path('', core_views.HomeView.as_view(), name='home'),
]
