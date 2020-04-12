from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from application.sap.views import (
    auth,
    feedback, 
    root,
    statistics,
    user,
)
from application.sap.views.api import (
    feedback as fb,
    stat,
    telegram,
)


urlpatterns = [
    path('', root.index, name='root-index'),
    path('help/', root.help, name='root-help'),

    path('auth/signup/', auth.signup, name='auth-signup'),
    path('auth/signin/', auth.signin, name='auth-signin'),
    path('auth/signout/', auth.signout, name='auth-signout'),

    path('user/profile/<username>/', user.profile, name='user-profile'),
    path('user/settings/', user.settings, name='user-settings'),

    path('statistics/', statistics.index, name='statistics-index'),
    path('statistics/commented/', statistics.commented, name='statistics-commented'),
    path('statistics/estimated/', statistics.estimated, name='statistics-estimated'),
    path('statistics/estimated/bygroup/', statistics.estimated_by_group, name='statistics-estimated-by-group'),
    path('statistics/estimated/byday/', statistics.estimated_by_day, name='statistics-estimated-by-day'),

    path('feedback/create/', feedback.create, name='feedback-create'),
    path('feedback/get/<fb_type>/<hash>/', feedback.get, name='feedback-get'),

    path('api/telegrambot/send/', telegram.BotSender.as_view(), name='api-bot_send'),
    path('api/statistics/comments/', stat.Comments.as_view(), name='api-stat-comments'),
    path('api/statistics/group/average/', stat.GroupAverage.as_view(), name='api-stat_group_average'),
    path('api/statistics/group/day/info/', stat.GroupDayInfo.as_view(), name='api-stat_group_day_info'),
    path('api/feedback/get/commented/', fb.Commented.as_view(), name='api-feedback_commented'),
    path('api/feedback/get/estimated/', fb.Estimated.as_view(), name='api-feedback_estimated'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
