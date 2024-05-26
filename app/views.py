from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

from app.answers import Answer
from app.questions import Question
from app.models import get_pagination_array
from app.forms import RegisterForm, LoginForm, AddQuestionForm, AddAnswerForm


def index(request):
    return render(request, 'index.html', context=get_pagination_array(request, Question.objects.get_new()))


def hot(request):
    return render(request, 'hot.html', context=get_pagination_array(request, Question.objects.get_hot()))


def question(request, question_id):
    question_item = Question.objects.get_by_id(question_id)
    context = get_pagination_array(request, Answer.objects.get_by_question(question_id))
    context['question'] = question_item
    return render(request, 'question_detail.html', context=context)


def tag(request, selected_tag):
    context = get_pagination_array(request, Question.objects.get_by_tag(selected_tag))
    context['selected_tag'] = selected_tag
    return render(request, 'tag.html', context=context)


def ask(request):
    if request.method == 'GET':
        question_form = AddQuestionForm()
    if request.method == 'POST':
        question_form = AddQuestionForm(request.POST)
        if request.user.is_authenticated:
            if question_form.is_valid():
                question = question_form.save()
                if question:
                    if 'continue' in request.GET:
                        return redirect(request.GET['continue'])
                    else:
                        return redirect(reverse('index'))
                else:
                    question_form.errors['__all__'] = question_form.non_field_errors('error')
        else:
            question_form.add_error('', 'Log in')
    return render(request, 'ask.html', {'question_form': question_form})


def signup(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    if request.method == 'POST':
        user_form = RegisterForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.errors['__all__'] = user_form.non_field_errors('error')
    return render(request, 'sign_up.html', {'form': user_form})


def login(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                login(request, user)
                if 'continue' in request.GET:
                    return redirect(request.GET['continue'])
                else:
                    return redirect(reverse('index'))
        else:
            login_form.errors['__all__'] = ['Неверный логин или пароль.']
    return render(request, 'login.html', {'form': login_form})


def logout(request):
    logout(request)
    return redirect(request.GET['continue'])


def settings(request):
    return render(request, 'settings.html')


def page_404(req, exc):
    return HttpResponseNotFound('<h1> Page not found :( </h1>')

def answer_question(request, question_id):
    question = Question.objects.get(pk=question_id)

    if request.method == 'POST':
        form = AddAnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()

            return redirect('question_detail', question_id=question_id)
    else:
        form = AddAnswerForm()

    context = {
        'question': question,
        'form': form,
    }

    return render(request, 'answer_question.html', context)