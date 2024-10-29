from django.shortcuts import get_object_or_404, render
from django.utils.timezone import localdate

from blog.models import Category, Post
from .constants import POST_LIST_SIZE


def get_post_list(category=None):
    post_list = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        pub_date__lte=localdate()
    )
    if category:
        return post_list.filter(category=category)
    return post_list.filter(category__is_published=True)


def index(request):
    template = 'blog/index.html'
    post_list = get_post_list()[:POST_LIST_SIZE]
    context = {'post_list': post_list[::-1]}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(get_post_list(), pk=post_id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post_list = get_post_list(category)
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
