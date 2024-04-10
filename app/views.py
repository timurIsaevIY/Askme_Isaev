from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger

from app import models


# Create your views here.


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    count = paginator.num_pages
    try:
        page_num = int(request.GET.get('page', 1))
        if page_num <= 0:
            page_num = 1
        elif page_num > count:
            page_num = count
    except:
        page_num = 1
    page_obj = paginator.page(page_num)
    paginator_elements = [i for i in range(max(page_num - 4, 1), min(page_num + 4, count) + 1)]
    return [page_obj, page_num, count, paginator_elements]


def index(request):
    return render(request, 'index.html', context=models.get_pagination_array(request, models.Question.objects.get_new()))


def hot(request):
    return render(request, 'hot.html', context=models.get_pagination_array(request,models.Question.objects.get_hot()))


def question(request, question_id):
    question_item = models.Question.objects.get_by_id(question_id)
    context = models.get_pagination_array(request,models.Answer.objects.get_by_question(question_id))
    context['question'] = question_item
    return render(request, 'question_detail.html', context=context)


def tag(request, selected_tag):
    context = models.get_pagination_array(request, models.Question.objects.get_by_tag(selected_tag))
    context['selected_tag'] = selected_tag
    return render(request, 'tag.html', context=context)


def ask(request):
    return render(request, 'ask.html')


def signup(request):
    return render(request, 'sign_up.html')


def login(request):
    return render(request, 'login.html')


def settings(request):
    return render(request, 'settings.html')


def page_404(req, exc):
    return HttpResponseNotFound('<h1> Page not found :( </h1>')
