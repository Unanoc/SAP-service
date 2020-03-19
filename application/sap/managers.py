from django.contrib.auth.models import UserManager
from django.db import connection, models


class UserManager(UserManager):

    def by_username(self, username):
        return self.all().filter(username=username).first()


class FeedbackSettingsManager(models.Manager):

    def get_by_hash(self, hash):
        return self.all().filter(hash_url=hash).first()

    def get_where(self, **kwargs):
        return self.all().filter(**kwargs).first()


class CommentedFeedbackManager(models.Manager):

    def get_group_comments_for_day(self, user_id, date, group, subject):
        with connection.cursor() as cursor:
            query = """
                SELECT text, group_name, subject, date
                FROM sap_commentedfeedback as s
                WHERE
                    s.user_id = '{}' AND s.group_name = '{}' AND s.subject = '{}'
                    AND s.date = '{}'
            """.format(user_id, group, subject, date)

            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                obj = {
                    'text': row[0], 
                    'group_name': row[1],
                    'subject': row[2],
                    'date': row[3],
                }
                result_list.append(obj)
        return result_list


class EstimatedFeedbackManager(models.Manager):

    def get_group_average(self, user_id, date_from, date_to, group, subject):
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
    
    def get_group_day_info(self, user_id, date, group, subject):
        with connection.cursor() as cursor:
            query = """
                SELECT s.rating, time
                FROM sap_estimatedfeedback as s
                WHERE 
                    s.user_id = '{}' AND s.group_name = '{}' AND s.subject = '{}'
                    AND s.date = '{}'
            """.format(user_id, group, subject, date)

            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                result_list.append({'rating': row[0], 'time': row[1].strftime("%H:%M:%S")})
        return result_list
    