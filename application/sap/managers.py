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

    def get_group_comments_for_day(self, user_id, date, group_name, subject):
        with connection.cursor() as cursor:
            query = """
                SELECT c.text, c.date, c.time
                FROM sap_commentedfeedback c
                JOIN sap_feedbacksettings f
                ON f.id = c.settings_id AND f.date = '{}' AND f.subject = '{}' 
                AND f.user_id = '{}' AND f.group_name = '{}'
                ORDER BY c.time DESC
            """.format(date, subject, user_id, group_name)

            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                obj = {
                    'text': row[0], 
                    'date': row[1], 
                    'time': row[2].strftime("%H:%M:%S"), 
                }
                result_list.append(obj)
        return result_list


class EstimatedFeedbackManager(models.Manager):

    def get_group_average(self, user_id, date_from, date_to, group_name, subject):
        with connection.cursor() as cursor:
            query = """
                SELECT AVG(s.rating), s.date
                FROM sap_estimatedfeedback as s
                WHERE 
                    s.user_id = '{}' AND s.group_name = '{}' AND s.subject = '{}'
                    AND s.date >= '{}' AND s.date <= '{}'
                GROUP BY date
                ORDER BY date
            """.format(user_id, group_name, subject, date_from, date_to)

            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                obj = {'avg_rating': row[0], 'date': row[1]}
                result_list.append(obj)
        return result_list
    
    def get_group_day_info(self, user_id, date, group_name, subject):
        with connection.cursor() as cursor:
            query = """
                SELECT s.rating, s.time, s.comment
                FROM sap_estimatedfeedback as s
                WHERE 
                    s.user_id = '{}' AND s.group_name = '{}' AND s.subject = '{}'
                    AND s.date = '{}'
                ORDER BY s.time
            """.format(user_id, group_name, subject, date)

            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                result_list.append(
                    {
                        'rating': row[0], 
                        'time': row[1].strftime("%H:%M:%S"),
                        'comment': row[2],
                    }
                )
        return result_list
    