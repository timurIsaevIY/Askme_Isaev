from _datetime import datetime
from django.contrib.auth.models import User
from django.db import models

from app.views import paginate


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-upload_date')

    def get_hot(self):
        return self.order_by('-likes')

    def get_all(self):
        return self.order_by()

    def get_by_id(self, question_id):
        return self.get(id=question_id)

    def get_by_tag(self, tag_title):
        return self.filter(tags__title=tag_title)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    likes = models.IntegerField(default=0)
    user = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)

    objects = QuestionManager()

    def __str__(self):
        return self.title + ' ' + str(self.id)


class AnswerManager(models.Manager):
    def get_all(self):
        return self

    def get_by_question(self, question_id):
        return self.filter(question_id=question_id)

    def get_count_by_questions(self, questions):
        answers = {}
        for question in questions:
            answers[question.id] = self.filter(question_id=question.id).count()
        return answers


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField()
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    objects = AnswerManager()
    likes = models.IntegerField(default=0)


class TagManager(models.Manager):
    def get_popular(self):
        return self.order_by()[:10]

    def get_by_question(self, question):
        return self.filter(questions=question)


class Tag(models.Model):
    title = models.CharField(max_length=100)
    objects = TagManager()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = (('user', 'question'),)


class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'answer'),)


def get_pagination_array(request, obj, ):
    arr_paginate = paginate(obj, request)
    answers = models.Answer.objects.get_count_by_questions(arr_paginate[0])
    context = {
        'questions': arr_paginate[0],
        'tags': models.Tag.objects.get_popular(),
        'answers': answers,
        'current_page': arr_paginate[1],
        'pages_count': arr_paginate[2],
        'paginator': arr_paginate[3]
    }
    return context
