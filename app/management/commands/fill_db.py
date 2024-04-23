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
            profiles.append(Profile.objects.create(user=user, avatar=random.choice(avatars), pk=user.pk + 100))
        Profile.objects.bulk_create(profiles)

        tags = [fake_name.word() for i in range(ratio)]
        for tag in tags:
            Tag.objects.create(title=tag)
        Tag.objects.bulk_create(tags)

        questions = []
        for i in range(ratio * 10):
            question = Question.objects.create(
                title=fake_name.text(max_nb_chars=50),
                text=fake_name.text(max_nb_chars=250),
                upload_date=datetime.now(),
                user=random.choice(profiles)
            )
            question.tags.set(random.sample(tags, random.randint(1, 4)))
            questions.append(question)
        Question.objects.bulk_create(questions)

        answers = []
        for i in range(ratio * 100):
            answer = Answer.objects.create(
                user=random.choice(profiles),
                question=random.choice(questions),
                text=fake_name.text(max_nb_chars=250),
                upload_date=datetime.now(),
                is_answer=random.choice([True, False])
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)

        answerLikes = []
        questionLikes = []
        for i in range(ratio * 100):
            question_index = random.randint(0, len(questions) - 1)
            answer_index = random.randint(0, len(answers) - 1)
            questionLike = QuestionLike.objects.create(
                question=questions[question_index],
                user=random.choice(profiles),
                is_like=random.choices([True, False])
            )
            answerLike = AnswerLike.objects.create(
                answer=answers[answer_index],
                user=random.choice(profiles),
                is_like=random.choices([True, False])
            )
            questionLikes.append(questionLike)
            answerLikes.append(answerLike)

            if questionLike.is_like:
                questions[question_index].likes += 1
            else:
                questions[question_index].likes -= 1

            if answerLike.is_like:
                answers[answer_index].likes += 1
            else:
                answers[answer_index].likes -= 1
        QuestionLike.objects.bulk_create(questionLikes)
        AnswerLike.objects.bulk_create(answerLikes)
        for question in questions:
            Question.objects.filter(id=question.id).update(likes=question.likes)

        for answer in answers:
            Answer.objects.filter(id=answer.id).update(likes=answer.likes)
