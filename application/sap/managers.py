from django.contrib.auth.models import UserManager
from django.db import models


class UserManager(UserManager):

    def by_username(self, username):
        return self.all().filter(username=username).first()


class CommentedFeedbackSettingsManager(models.Manager):

    def get_by_hash(self, hash):
        return self.all().filter(hash_url=hash).first()