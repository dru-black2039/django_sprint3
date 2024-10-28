from django.shortcuts import get_object_or_404, render
from django.utils.timezone import localdate

from blog.models import Category, Post


def get_post_list(category_slug=None):
    post_list = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=localdate()
    )
    if category_slug:
        return post_list.filter(category__slug=category_slug)
    return post_list


def index(request):
    template = 'blog/index.html'
    post_list = get_post_list().order_by('-id')[0:5]
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
    post_list = get_post_list(category_slug)
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
