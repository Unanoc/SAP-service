from django.contrib.auth.models import UserManager
from django.db import models


class UserManager(UserManager):

    def by_username(self, username):
        return self.all().filter(username=username).first()


class FeedbackSettingsManager(models.Manager):

    def get_by_hash(self, hash):
        return self.all().filter(hash_url=hash).first()

    def get_where(self, **kwargs):
        return self.all().filter(**kwargs).first()


class CommenterFeedbackManager(models.Manager):

    pass


class EstimatedFeedbackManager(models.Manager):

    def get_group_average(self, user_id, date_from, date_to, group, subject):
        from django.db import connection
        with connection.cursor() as cursor:
            query = """
                SELECT AVG(s.rating), s.date
                FROM sap_estimatedfeedback as s
                WHERE 
                    s.user_id = '{}' AND s.group_name = '{}' AND s.subject = '{}'
                    AND s.date >= '{}' AND s.date <= '{}'
                GROUP BY date
                ORDER BY date
            """.format(user_id, group, subject, date_from, date_to)

            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                obj = {'avg_rating': row[0], 'date': row[1]}
                result_list.append(obj)
        return result_list
