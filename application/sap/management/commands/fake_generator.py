import calendar
import datetime
import random
from django.core.management.base import BaseCommand
from faker import Faker

from application.sap.models import (
    EstimatedFeedback,
    User,
)

# To clean up Data base and generate fake data just write "python manage.py flush && python manage.py fake_generator"

count_estimated_feedback = 30

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.user_generate()
        self.estimated_feedback_generate()


    def user_generate(self):
        faker = Faker()
        username = "test"
        user = User.objects.create_user(username=username, password=username)
        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.save()

    def get_dates_of_current_month(self):
        today = datetime.datetime.today()
        month_range = calendar.monthrange(today.year, today.month)
        template = "{}-{}-{}"

        for i in range(1, month_range[1]+1):
            yield template.format(today.year, today.month, i)



    def estimated_feedback_generate(self):
        faker = Faker()
        user = User.objects.by_username('test')

        for date in self.get_dates_of_current_month():
            for subject in ['Электроника', 'ООП', 'Схемотехника', 'Дискретная математика', 'Информатика']:
                for group in ["ИУ6-8{}".format(i) for i in range(1, 6)]:
                    for i in range(1, count_estimated_feedback):
                        estimated_feedback = EstimatedFeedback.objects.create(
                            rating=random.randint(1, 5), 
                            comment=faker.sentence(),
                            group_name=group,
                            subject=subject,
                            date=date,
                            user_id=user.id,
                        )
                        estimated_feedback.save()
