import uuid
import calendar
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from faker import Faker

from application.sap.models import (
    CommentedFeedback,
    EstimatedFeedback,
    FeedbackSettings,
    User,
)

# To clean up Database and generate fake data, just write "python manage.py flush && python manage.py fake_generator"

students_num = 20
subject_name = "Программирование на языке С/С++"
class_type = ["Лекция", "Семинар"]
student_group = "ИУ6-84Б"
class_days = [2, 7, 9, 14, 16, 21, 23, 28, 30]
chat_name = "@sap_test_channel"
test_comments = [
    "Очень интересное занятие! Много нового узнал.",
    "Было плохо слышно, из-за этого мало материала усвоил на занятии:(",
    "Очень быстро проходим каждый раздел, не успевает закрепиться в голове...",
    "Сегодня было очень здорово интересно",
    "Хорошая подача материала, спасибо большое!",
    "Не структурированный материал, поэтому было сложно уловить концепцию",
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.user_generate()
        self.feedback_generate()


    def user_generate(self):
        faker = Faker()
        username = "test"
        password = "test"
        user = User.objects.create_user(username=username, password=password)
        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.save()


    def get_dates_of_current_month(self):
        today = datetime.today()
        month_range = calendar.monthrange(today.year, today.month)
        template = "{}-{}-{}"

        for i in range(1, month_range[1]+1):
            yield template.format(today.year, today.month, i)


    def feedback_generate(self):
        faker = Faker()
        user = User.objects.by_username('test')

        for day, date in enumerate(self.get_dates_of_current_month()):
            if day+1 not in class_days:
                continue

            hash_commented = uuid.uuid4()
            hash_estimated = uuid.uuid4()

            fs_commented = FeedbackSettings.objects.create(
                group_name=student_group,
                subject=subject_name,
                class_type=random.choice(class_type),
                chat_name=chat_name,
                feedback_type="commented",
                url="/feedback/get/{}/{}".format("commentes", hash_commented),
                _hash=hash_commented,
                user=user,
                date=date,
            )
            fs_commented.save()

            fs_estimated = FeedbackSettings.objects.create(
                group_name=student_group,
                subject=subject_name,
                class_type=random.choice(class_type),
                chat_name=chat_name,
                feedback_type="estimated",
                url="/feedback/get/{}/{}".format("estimated", hash_estimated),
                _hash=hash_estimated,
                user=user,
                date=date,
            )
            fs_estimated.save()

            for i in range(1, students_num):
                test_comment_index = i % len(test_comments)
                commented_feedback = CommentedFeedback.objects.create(
                    text=test_comments[test_comment_index],
                    date=date,
                    settings=fs_commented,
                )
                commented_feedback.save()

                estimated_feedback = EstimatedFeedback.objects.create(
                    rating=random.randint(1, 5), 
                    text=test_comments[test_comment_index],
                    date=date,
                    settings=fs_estimated,
                )
                estimated_feedback.save()
