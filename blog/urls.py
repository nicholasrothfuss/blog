from django.contrib import admin
from django.urls import path
from blog.apps.engine import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.HomePostListView.as_view(), name='home'),
]
