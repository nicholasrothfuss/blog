from django.views.generic import ListView, DateDetailView
from .models import Post


class HomePostListView(ListView):
    context_object_name = 'posts'
    template_name = 'home.html'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)


class PermalinkView(DateDetailView):
    context_object_name = 'post'
    date_field = 'published_at'
    month_format = '%m'
    template_name = 'permalink.html'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)
