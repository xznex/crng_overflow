from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app.forms import LoginForm, SignupForm, SettingsForm, AskForm, AnswerForm
from .models import *


def paginate(object_list, request, limit=3):
    paginator = Paginator(object_list, limit)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


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
    t = Tag.objects.all()
    return render(request, 'app/tag.html', {'question': q, 'hot_tags': ht, 'tag_url': tag_url, 'tags': t})


def question(request, pk):
    q = Question.objects.get(pk=pk)
    a = Answer.objects.by_question(pk)
    t = Tag.objects.all()
    form = AnswerForm()
    if request.user.is_authenticated and request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = request.POST.get('answer')
            user = User.objects.get(id=request.user.pk)
            profile = Profile.objects.get(user=user)
            ans = Answer.objects.create(profile=profile, question=q, text=answer)
            ans.save()
            form = AnswerForm()

    return render(request, 'app/question_page.html', {'question': q, 'answers': a, 'tags': t, 'form': form})


def login_view(request):
    t = Tag.objects.all()
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, "User not found.")
            else:
                login(request, user)
                return redirect(reverse('index'))

    return render(request, 'registration/login.html', {'form': form, 'tags': t})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/?continue=logout')


def signup_view(request):
    t = Tag.objects.all()
    if request.method == 'GET':
        form = SignupForm()
    elif request.method == 'POST':
        form = SignupForm(data=request.POST)
        print(request.POST.get("upload_avatar"))
        print(request.POST.get("username"))
        if form.is_valid():
            print(request.POST)
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            upload_avatar = request.POST.get("upload_avatar")

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user_pk = User.objects.get(id=user.pk)
            add_avatar = Profile(user=user_pk, avatar=upload_avatar)
            add_avatar.save()

            login(request, user)

            return redirect('index')
    return render(request, 'registration/signup.html', {'form': form, 'tags': t})


@login_required()
def settings(request):
    t = Tag.objects.all()
    if request.method == 'GET':
        form = SettingsForm()
    elif request.method == 'POST':
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            print(request.POST)
            username = request.POST.get("username")
            email = request.POST.get("email")
            new_avatar = request.POST.get("upload_avatar")
            request.user.username = username
            request.user.email = email
            request.user.profile.avatar = new_avatar
            request.user.save()
            form = SettingsForm()
            # user = User.objects.create_user(username=username, email=email)
            # user.save()
            # user_pk = User.objects.get(id=user.pk)
            # add_avatar = Profile(user=user_pk, avatar=upload_avatar)
            # add_avatar.save()
    return render(request, 'app/settings.html', {'form': form, 'tags': t})


@login_required()
def ask(request):
    t = Tag.objects.all()
    if request.method == 'GET':
        form = AskForm()
    elif request.method == 'POST':
        form = AskForm(data=request.POST)
        if form.is_valid():
            title = request.POST.get("title")
            text = request.POST.get("text")
            user = User.objects.get(id=request.user.pk)
            profile = Profile.objects.get(user=user)
            q = Question.objects.create(profile=profile, title=title, text=text)
            tags = request.POST.get("tags").split(",")
            for t in tags:
                t = str(t).replace(' ', '')
                Tag.objects.get_or_create_tag(t, q)
            q.save()
            return redirect('question', pk=q.id)
    return render(request, 'app/ask.html', {'form': form, 'tags': t})


def page_not_found(request, exception):
    return render(request, 'app/page_not_found.html', status=404)
