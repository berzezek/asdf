from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


# Create your views here.

def post_share(request, post_id):
    post = get_object_or_404(Post , pk=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})

def post_list(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        post_list = paginator.get_page(page_number)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        post_list = paginator.page(1)

    return render(request,
                  'blog/post/list.html',
                  {'posts': post_list})


def post_detail(request, post, year, month, day):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
