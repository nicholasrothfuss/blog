from django import template
from ..models import Post


register = template.Library()


@register.inclusion_tag('_post.html')
def render_posts(posts, header_tag='h2', list_categories=True, include_permalink=True):
    if isinstance(posts, Post):
        posts = [posts]
    return {
        'posts': posts,
        'header_tag': header_tag,
        'list_categories': list_categories,
        'include_permalink': include_permalink,
    }
