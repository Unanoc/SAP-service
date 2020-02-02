from django.contrib.auth.models import UserManager


class UserManager(UserManager):

    def by_username(self, username):
        return self.all().filter(username=username).first()
