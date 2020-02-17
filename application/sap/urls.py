from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from application.sap import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),
    path('profile/<username>/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('create/poll/', views.create_poll, name='create_poll'),
    path('statistics/', views.statistics, name='statistics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)