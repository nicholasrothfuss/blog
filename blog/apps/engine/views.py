from django.views.generic import ListView
from .models import Post


class HomePostListView(ListView):
    context_object_name = 'posts'
    template_name = 'home.html'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)
