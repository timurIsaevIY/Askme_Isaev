from django.urls import path

from app import views
from app.views import page_404

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path('tag//<selected_tag>', views.tag, name='tag'),
    path('question/<int:question_id>/answer/', views.answer_question, name='answer_question')
]
handler404 = page_404
