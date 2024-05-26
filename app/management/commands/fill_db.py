import random
from datetime import datetime

from django.core.management.base import BaseCommand
from faker import Faker
from app.models import User, Profile, Tag, Question, Answer, QuestionLike, AnswerLike


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        fake_name = Faker()
        users = []
        for i in range(ratio):
            username = fake_name.unique.name()
            user = User.objects.create(username=username)
            users.append(user)
        avatars = []
        for i in range(16):
            avatars.append("static/img/avatars/" + str(i) + ".png")
        profiles = []
        for user in users:
            profiles.append(Profile(user=user, avatar=random.choice(avatars)))
        Profile.objects.bulk_create(profiles)
        print("profile created")
        tags = [fake_name.word() for i in range(ratio)]
        tags_obj = []
        for tag in tags:
            tags_obj.append(Tag(title=tag))
        Tag.objects.bulk_create(tags_obj)
        print("tag created")
        questions = []
        for i in range(ratio * 10):
            question = Question(
                title=fake_name.text(max_nb_chars=50),
                text=fake_name.text(max_nb_chars=250),
                upload_date=datetime.now(),
                user=random.choice(profiles)
            )
            questions.append(question)
        Question.objects.bulk_create(questions)
        print("question created")
        for question in Question.objects.all():
            question.tags.set(random.sample(tags_obj, random.randint(1, 4)))
        answers = []
        for i in range(ratio * 100):
            answer = Answer(
                user=random.choice(profiles),
                question=random.choice(questions),
                text=fake_name.text(max_nb_chars=250),
                upload_date=datetime.now(),
                is_correct=bool(random.choice([True, False]))
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)
        print("answer created")
        answerLikes = []
        questionLikes = []
        for profile in profiles:
            question_index = random.sample(range(len(questions)), 100)
            answer_index = random.sample(range(len(answers)), 100)
            for i in range(100):
                questionLike = QuestionLike(
                    question=questions[question_index[i]],
                    user=profile,
                    is_like=bool(random.choices([True, False]))
                )
                answerLike = AnswerLike(
                    answer=answers[answer_index[i]],
                    user=profile,
                    is_like=bool(random.choices([True, False]))
                )
                questionLikes.append(questionLike)
                answerLikes.append(answerLike)

                if questionLike.is_like:
                    questions[question_index[i]].likes += 1
                else:
                    questions[question_index[i]].likes -= 1

                if answerLike.is_like:
                    answers[answer_index[i]].likes += 1
                else:
                    answers[answer_index[i]].likes -= 1
        print("question likes created")
        QuestionLike.objects.bulk_create(questionLikes)
        AnswerLike.objects.bulk_create(answerLikes)
        print("answer likes created")
        for question in questions:
            Question.objects.filter(id=question.id).update(likes=question.likes)
        print("question likes updated")
        for answer in answers:
            Answer.objects.filter(id=answer.id).update(likes=answer.likes)
        print("answer likes updated")