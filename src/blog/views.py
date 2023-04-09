from django.shortcuts import render,get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import *

# Create your views here.

def category_view(request, slug):
    queryset = category.objects.filter(slug=slug).all()
    template_name = 'blog/garden-category.html'
    context = { 'queryset': queryset }
    return render(request, template_name, context)


def home_view(request):
    categories = category.objects.all()
    blog = Blog.objects.all().first()
    #pagination
    queryset = Post.objects.filter(post_status='published')
    search_query = request.GET.get('search')
    if search_query:
        queryset = Post.objects.filter(
            Q(post_title__icontains=search_query)
        )
    per_page = 2
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    #featured_post
    featured_one = Post.objects.filter(featured_post=True)[:1].get()
    featured_two = Post.objects.filter(featured_post=True)[1:2].get()
    featured_three = Post.objects.filter(featured_post=True)[2:3].get()

    
    context = {
        'posts': posts,
        'blog': blog,
        'featured_one': featured_one,
        'featured_two': featured_two,
        'featured_three': featured_three,
        'categories': categories,

    }
    template_name = 'blog/garden-index.html'
    return render(request, template_name , context)


def single_view(request, slug):
    all_post = Post.objects.filter(post_status='published')[:4]
    blogs = Blog.objects.all().first()
    post = get_object_or_404(Post, slug=slug)
    all_category = category.objects.all()
    
    #comment section
    myPost = get_object_or_404(Post, slug=slug)
    comments = myPost.comments.filter(active=True)
    new_comment = None
    #Comment Post
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = myPost
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = { 'post': post, 'all_post': all_post, 'blogs': blogs, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'all_category': all_category }
    template_name = 'blog/garden-single.html'
    return render(request, template_name, context)
    