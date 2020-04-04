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

# To clean up Data base and generate fake data just write "python manage.py flush && python manage.py fake_generator"

count_estimated_feedback = 10
count_commented_feedback = 10

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

        for date in self.get_dates_of_current_month():
            for subject in ['Электроника', 'ООП', 'Схемотехника', 'Дискретная математика', 'Информатика']:
                for group in ["ИУ6-8{}".format(i) for i in range(1, 6)]:
                    hash_url = uuid.uuid4()

                    fs_commented = FeedbackSettings.objects.create(
                        group_name=group,
                        subject=subject,
                        user=user,
                        telegram_channel="test_channel",
                        base_url="test_commented_url",
                        hash_url=hash_url,
                        date=date,
                    )
                    fs_commented.save()

                    fs_estimated = FeedbackSettings.objects.create(
                        group_name=group,
                        subject=subject,
                        user=user,
                        telegram_channel="test_channel",
                        base_url="test_estimated_url",
                        hash_url=hash_url,
                        date=date,
                    )
                    fs_estimated.save()

                    for i in range(1, count_estimated_feedback):
                        commented_feedback = CommentedFeedback.objects.create(
                            text=faker.sentence(),
                            group_name=group,
                            subject=subject,
                            date=date,
                            user_id=user.id,
                            settings=fs_commented,
                        )
                        commented_feedback.save()

                        estimated_feedback = EstimatedFeedback.objects.create(
                            rating=random.randint(1, 5), 
                            comment=faker.sentence(),
                            group_name=group,
                            subject=subject,
                            date=date,
                            user_id=user.id,
                            settings=fs_estimated,
                        )
                        estimated_feedback.save()