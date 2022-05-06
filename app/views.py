from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import *


def paginate(object_list, request, limit=3):
    paginator = Paginator(object_list, limit)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


def base(request):
    t = Tag.objects.hot_tags()
    return render(request, 'app/index.html', {'tags': t})


def index(request):
    q = paginate(Question.objects.all(), request)
    t = Tag.objects.all()
    return render(request, 'app/index.html', {'question': q, 'tags': t})


def hot(request):
    q = paginate(Question.objects.hot(), request)
    t = Tag.objects.all()
    return render(request, 'app/hot.html', {'question': q, 'tags': t})


def tag(request, tag_url):
    ht = Tag.objects.hot_tags()
    q = Question.objects.by_tag(tag_url)
    return render(request, 'app/tag.html', {'question': q, 'hot_tags': ht, 'tag_url': tag_url})


def question(request, pk):
    q = Question.objects.get(pk=pk)
    a = Answer.objects.by_question(pk)
    t = Tag.objects.all()
    return render(request, 'app/question_page.html', {'question': q, 'answers': a, 'tags': t})


def login(request):
    return render(request, 'app/login.html')


def signup(request):
    return render(request, 'app/signup.html')


def settings(request):
    return render(request, 'app/settings.html')


def ask(request):
    return render(request, 'app/ask.html')


def page_not_found(request, exception):
    return render(request, 'app/page_not_found.html', status=404)

