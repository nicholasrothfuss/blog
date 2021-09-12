from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DateDetailView
from .models import Category, Post


class CategoryArchiveView(ListView):
    context_object_name = 'posts'
    template_name = 'category_archive.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.posts.filter(status=Post.Status.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class HomePostListView(ListView):
    context_object_name = 'posts'
    template_name = 'home.html'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).prefetch_related('categories')


class PermalinkView(DateDetailView):
    context_object_name = 'post'
    date_field = 'published_at'
    month_format = '%m'
    template_name = 'permalink.html'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)
