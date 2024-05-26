from django.db import models


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