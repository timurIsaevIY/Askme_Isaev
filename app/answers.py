from django.db import models
from app.questions import Question


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