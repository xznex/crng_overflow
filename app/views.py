from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_POST

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
    q = paginate(Question.objects.by_tag(tag_url), request)
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

    return render(request, 'app/question_page.html',
                  {'question': q, 'answers': a, 'tags': t, 'form': form})


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
    else:
        form = SignupForm(data=request.POST, files=request.FILES)
        print(request.FILES.get("upload_avatar"))
        print(request.POST.get("username"))
        if form.is_valid():
            print(request.POST)
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            upload_avatar = request.FILES.get("upload_avatar")
            duplicate_check = User.objects.filter(username=username).exists()
            if duplicate_check:
                form.add_error(0, "Duplicate login.")
            else:
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
        form = SettingsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            print(request.FILES)
            username = request.POST.get("username")
            email = request.POST.get("email")
            new_avatar = request.FILES.get("new_avatar")
            request.user.username = username
            request.user.email = email
            duplicate_check = User.objects.filter(username=username).exists()
            if duplicate_check:
                form.add_error(0, "Choose another login.")
            else:
                request.user.save()
                user_obj = User.objects.get(id=request.user.pk)
                profile_obj = Profile.objects.get(user=user_obj)
                profile_obj.avatar = new_avatar
                profile_obj.save()
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


@login_required
@require_POST
def vote(request):
    print(request.POST)
    question_id = request.POST["id"]
    answer = request.POST["answer"]
    quest = Question.objects.get(id=question_id)

    check(request, answer, quest)



    # return JsonResponse({'pointer_events': True})
    return JsonResponse({})


@login_required
@require_POST
def comment_vote(request):
    print(request.POST)
    answer_id = request.POST["id"]
    answer = request.POST["answer"]
    ans = Answer.objects.get(id=answer_id)

    check_answer(request, answer, ans)

    return JsonResponse({})


@login_required
@require_POST
def correct(request):
    print(request.POST)
    answer_id = request.POST["id"]
    ans = Answer.objects.get(id=answer_id)
    print(ans.is_correct)
    ans.is_correct = not ans.is_correct
    ans.save()
    print(ans.is_correct)
    return JsonResponse({})


def check_answer(request, answer, ans):
    user_profile = Profile.objects.get(user=request.user)
    try:
        LikeAnswer.objects.get(answer=ans, profile=user_profile)
    except ObjectDoesNotExist:
        if answer == "like":
            is_like = True
            ans.likes_count += 1
            ans.rating += 1
        else:
            is_like = False
            ans.dislikes_count += 1
            if ans.rating > 0:
                ans.rating -= 1
        ans.save()
        like_answer = LikeAnswer(answer=ans, profile=user_profile, is_like=is_like)
        like_answer.save()


def check(request, answer, quest):
    user_profile = Profile.objects.get(user=request.user)
    try:
        lq = LikeQuestion.objects.get(question=quest, profile=user_profile)
        print(lq.is_vote)
        # like_question.change_opinion()
    except ObjectDoesNotExist:
        if answer == "like":
            quest.likes_count += 1
            quest.rating += 1
        else:
            quest.dislikes_count += 1
            if quest.rating > 0:
                quest.rating -= 1
        is_vote = True
        quest.save()
        like_question = LikeQuestion(question=quest, profile=user_profile, is_vote=is_vote)
        like_question.save()
        print(like_question.is_vote)

        print(quest.is_vote_quest(user_profile))


def page_not_found(request, exception):
    return render(request, 'app/page_not_found.html', status=404)
