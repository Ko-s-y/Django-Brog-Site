from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Article, Comment, Tag
from blog.forms import CommentForm

def index(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 1)
    page_number = request.GET.get('page')
    context = {
        'pagi_articles': paginator.get_page(page_number),
        'page_number': page_number,
        'page_title': 'Django Blogs',
    }
    return render(request, 'blog/blogs.html', context)

def article(request, pk):
    article = Article.objects.get(id=pk)
    if request.method == 'POST':
        if request.POST.get('like_count', None):
            article.count += 1
            article.save()
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
    comments = Comment.objects.filter(article=article)
    context = {
        'article': article,
        'comments': comments,
    }
    return render(request, 'blog/article.html', context)

def tags(request, slug):
    tag = Tag.objects.get(slug=slug)
    articles = tag.article_set.all()
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    context = {
        'pagi_articles': paginator.get_page(page_number),
        'page_number': page_number,
        'page_title': 'Django Blogs #{}'.format(slug),
    }
    return render(request, 'blog/blogs.html', context)
