from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DateDetailView, MonthArchiveView, YearArchiveView
from django.views.generic.detail import DetailView
from .models import Category, Post


#-------------------#
#-- Mixin classes --#
#-------------------#

class PublishedPostMixin:
    date_field = 'published_at'

    def get_queryset(self):
        return Post.objects.published().prefetch_related('categories')


class SinglePublishedPostMixin(PublishedPostMixin):
    context_object_name = 'post'


class MultiplePublishedPostsMixin(PublishedPostMixin):
    context_object_name = 'posts'


#------------------#
#-- View classes --#
#------------------#

class HomeView(MultiplePublishedPostsMixin, ListView):
    template_name = 'home.html'


class PostCategoryArchiveView(MultiplePublishedPostsMixin, ListView):
    allow_empty = False
    template_name = 'category_archive.html'

    def get_queryset(self):      
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        qs = super().get_queryset()
        return qs.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    

class PostMonthArchiveView(MultiplePublishedPostsMixin, MonthArchiveView):
    month_format = '%m'
    template_name = 'month_archive.html'


class PostYearArchiveView(MultiplePublishedPostsMixin, YearArchiveView):
    make_object_list = True
    template_name = 'year_archive.html'


class PostPermalinkView(SinglePublishedPostMixin, DetailView):
    template_name = 'permalink.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            published_at__year=int(self.kwargs['year']),
            published_at__month=int(self.kwargs['month']),
            slug=self.kwargs['slug']
        )
    
