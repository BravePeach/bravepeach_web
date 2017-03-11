from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views



urlpatterns = [
    # index page
    url(r'^$', views.index, name='index'),

    # log-in and log-out
    url(r'login/$', auth_views.login, name='login',
        kwargs={'template_name': 'login.html'}),
    url(r'logout/$', views.user_logout, name='logout'),

    # password reset
    url(r'^password_reset/$',auth_views.password_reset,name="password_reset",
        kwargs={'template_name': 'password_reset.html',
                'email_template_name' : 'password_reset_email.html'}),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name="password_reset_done",
        kwargs={'template_name': 'password_reset_done.html'}),
    url(r'^password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm, name="password_reset_confirm",
        kwargs={'template_name': 'password_reset_confirm.html'}),
    url(r'^password_reset/complete$', auth_views.password_reset_complete, name="password_reset_complete",
        kwargs={'template_name': 'password_reset_complete.html'}),

    # user register
    url(r'^register/$', views.register, name='register'),

    # guide search
    url(r'^guide_search/$', views.guide_search, name='guide_search'),
    url(r'^guide_search/filtering/$', views.FilterGuide.as_view(), name='filter_guide'),

    # enroll trip
    url(r'^enroll_trip', views.enroll_trip, name='enroll_trip'),

    # edit user profile
    url(r'^edit/$',views.edit,name='edit'),
]