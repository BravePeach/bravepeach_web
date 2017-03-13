from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .forms import PasswordResetCustomForm, SetPasswordCustcomForm
from . import views

urlpatterns = [
    # Common
    url(r'^$', views.common.index, name='index'),

    # User
    url(r'^register/$', views.user.register, name='register'),
    url(r'^register_bravepeach/$', views.user.register_bravepeach, name="register_bp"),
    url(r'^check_email/$', views.user.check_email, name="check_email"),
    url(r'login/', views.user.user_login, name='login'),
    url(r'logout/$', views.user.user_logout, name='logout'),
    url(r'^edit/$', views.user.edit,name='edit'),
    url(r'^password_reset/$', auth_views.password_reset, name="password_reset",
        kwargs={'template_name': 'password_reset.html',
                'email_template_name': 'password_reset_email.html',
                "password_reset_form": PasswordResetCustomForm}),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name="password_reset_done",
        kwargs={'template_name': 'password_reset_done.html'}),
    url(r'^password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,
        name="password_reset_confirm", kwargs={'template_name': 'password_reset_confirm.html',
                                               "set_password_form": SetPasswordCustcomForm,
                                               "post_reset_redirect": "password_reset_complete"}),
    url(r'^password_reset/complete$', views.user.password_reset_complete, name="password_reset_complete"),

    # guide search
    url(r'^guide_search/$', views.trip.guide_search, name='guide_search'),
    url(r'^guide_search/filtering/$', views.trip.FilterGuide.as_view(), name='filter_guide'),

    # enroll trip
    url(r'^enroll_trip', views.trip.enroll_trip, name='enroll_trip'),

]
