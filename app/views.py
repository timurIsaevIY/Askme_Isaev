from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger

# Create your views here.

QUESTIONS = [
    {
        'id': str(i - 1),
        'title': f"Question number {i}",
        'text': f"This is the question number {i}"
    } for i in range(1,30)
]

def paginate(objects_list, request, per_page):
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
    return page_obj

def index(request):
    page_obj = paginate(QUESTIONS, request, 5)
    return render(request, 'index.html', {'questions': page_obj})

def hot(request):
    page_obj = paginate(QUESTIONS, request, 5)
    return render(request, 'hot.html', {'questions': page_obj})

def question(request, question_id):
    return render(request, 'question_detail.html', {'question': QUESTIONS[question_id]})

def ask(request):
    return render(request, 'ask.html')

def signup(request):
    return render(request, 'sign_up.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')