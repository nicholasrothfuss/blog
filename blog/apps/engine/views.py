from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DateDetailView
from .models import Category, Post


class PublishedPostMixin:
    def get_queryset(self):
        return Post.objects.published().prefetch_related('categories')


class CategoryArchiveView(PublishedPostMixin, ListView):
    context_object_name = 'posts'
    template_name = 'category_archive.html'

    def get_queryset(self):      
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        qs = super().get_queryset()
        return qs.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class HomePostListView(PublishedPostMixin, ListView):
    context_object_name = 'posts'
    template_name = 'home.html'


class PermalinkView(PublishedPostMixin, DateDetailView):
    context_object_name = 'post'
    date_field = 'published_at'
    month_format = '%m'
    template_name = 'permalink.html'
