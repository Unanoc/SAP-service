from django.contrib.auth.models import UserManager
from django.db import models


class UserManager(UserManager):

    def by_username(self, username):
        return self.all().filter(username=username).first()


class CommentedFeedbackManager(models.Manager):

    def get_by_id(self, question_id):
        return self.all().filter(id=question_id)