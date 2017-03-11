from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Common
    url(r'^$', views.common.index, name='index'),

    # User
    url(r'^register/$', views.user.register, name='register'),
    url(r'^register_bravepeach/$', views.user.register_bravepeach, name="register_bp"),
    url(r'login/$', auth_views.login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'logout/$', views.user.user_logout, name='logout'),
    url(r'^edit/$',views.user.edit,name='edit'),
    url(r'^password_reset/$', auth_views.password_reset, name="password_reset",
        kwargs={'template_name': 'password_reset.html',
                'email_template_name' : 'password_reset_email.html'}),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name="password_reset_done",
        kwargs={'template_name': 'password_reset_done.html'}),
    url(r'^password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm, name="password_reset_confirm",
        kwargs={'template_name': 'password_reset_confirm.html'}),
    url(r'^password_reset/complete$', auth_views.password_reset_complete, name="password_reset_complete",
        kwargs={'template_name': 'password_reset_complete.html'}),

    # guide search
    url(r'^guide_search/$', views.views.guide_search, name='guide_search'),
    url(r'^guide_search/filtering/$', views.views.FilterGuide.as_view(), name='filter_guide'),

    # enroll trip
    url(r'^enroll_trip', views.views.enroll_trip, name='enroll_trip'),

]
