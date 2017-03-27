from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from .forms import PasswordResetCustomForm, SetPasswordCustcomForm
from . import views

urlpatterns = [
    # Common
    url(r'^$', views.common.index, name='index'),

    # User
    url(r'^register/$', views.user.register, name='register'),
    url(r'^register_bravepeach/$', views.user.register_bravepeach, name="register_bp"),
    url(r'^greeting/$', views.user.greeting, name='greeting'),  # for test only
    url(r'^check_email/$', views.user.check_email, name="check_email"),
    url(r'^login', views.user.user_login, name='login'),
    url(r'^logout/$', views.user.user_logout, name='logout'),
    url(r"^mypage/(?P<page_type>\w+)/$", views.user.mypage, name="mypage"),
    url(r'^mypage/$', views.user.mypage, name='mypage_default'),
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
    url(r'^cert_mail/$', views.user.cert_mail, name='cert_mail'),
    url(r'^edit_profile/$', views.user.edit_profile, name="edit_profile"),
    url(r'^upload_original/$', views.user.upload_original, name='upload_original'),
    url(r'^upload_profile/$', views.user.upload_profile, name='upload_profile'),
    url(r'^unsub_bp/$', views.user.unsub_bp, name="unsub_bp"),

    # Guide
    url(r'^guide/$', views.guide.guide_index, name='guide_index'),
    url(r'^guide/(?P<gid>\d+)/$', views.guide.profile, name='guide_profile'),
    url(r'^trip_filtering/', views.guide.FilterTrip.as_view(), name='filter_trip'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/$', views.guide.write_offer, name='write_offer'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/search_accom/$', views.guide.search_accom, name='search_accom'),

    # User2Guide
    url(r'^guide_search/$', views.trip.guide_search, name='guide_search'),
    url(r'^filtering/$', views.trip.FilterGuide.as_view(), name='filter_guide'),
    url(r'^write_review/(?P<offer_id>\d+)/$', views.user.write_review, name="write_user_review"),

    # Trip
    url(r'^my_trip/$', views.trip.my_trip, name="my_trip"),
    url(r'^my_trip/(?P<user_request_id>\d+)/$', views.trip.volunteer_list, name="guide_list"),
    url(r'^offer/(?P<offer_id>\d+)/$', views.trip.offer_detail, name="offer_detail"),
    url(r'^enroll_trip/$', views.trip.enroll_trip, name='enroll_trip'),
    url(r'^cancel_offer/$', views.trip.cancel_offer, name="cancel_offer"),
    url(r'^payment/(?P<offer_id>\d+)/$', views.trip.payment, name="payment"),

    # Like
    url(r'^like/$', views.trip.like, name="like"),
    url(r'^add_like/$', views.trip.AddLike.as_view(), name="add_like"),
    url(r'^delete_like/$', views.trip.DeleteLike.as_view(), name="delete_like"),

    # Guide2User

    # Comment
    url(r'^add_comment/$', views.trip.AddComment.as_view(), name="add_comment"),

    url(r'^redactor', include('redactor.urls')),
]
