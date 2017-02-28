from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login/$', auth_views.login, name='user_login',
        kwargs={'template_name': 'login.html'}),
]
