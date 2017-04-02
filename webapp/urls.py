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
    url(r'^guide/$', views.guide.index, name='guide_index'),
    url(r'^guide/volunteer/$', views.guide.volunteer, name='guide_volunteer'),
    url(r'^guide/view-volunteer/(?P<gid>\d+)/$', views.guide.view_volunteer, name='view_volunteer'),
    url(r'^guide/enroll-volunteer/(?P<gid>\d+)/$', views.guide.enroll_volunteer, name='enroll_volunteer'),
    url(r'^guide/find/$', views.guide.find, name='guide_find'),
    url(r'^guide/dashboard/$', views.guide.dashboard, name='guide_dashboard'),
    url(r'^guide/schedule/$', views.guide.schedule, name='guide_schedule'),
    url(r'^guide/request/$', views.guide.request, name='guide_request'),
    url(r'^guide/adjust/$', views.guide.adjust, name='guide_adjust'),
    url(r'^guide/set-adjust/$', views.guide.set_adjust_method, name="set_adjust"),
    url(r'^guide/request-adjust/(?P<oid>\d+)/$', views.guide.request_adjust, name='request_adjust'),
    url(r'^guide/review/$', views.guide.review, name='guide_review'),
    url(r'^guide/write_review/(?P<oid>\d+)/$', views.guide.write_review, name="guide_write_review"),
    url(r'^guide/view_review/(?P<oid>\d+)/$', views.guide.view_review, name="guide_view_review"),
    url(r'^guide/write_journal/(?P<oid>\d+)/$', views.guide.write_journal, name="guide_write_journal"),
    url(r'^guide/view_journal/(?P<jid>\d+)/$', views.guide.view_journal, name="guide_view_journal"),
    url(r'^guide/template/$', views.guide.template, name='guide_template'),
    url(r'^guide/inactivate/$', views.guide.inactivate, name='guide_inactivate'),
    url(r'^guide/activate/$', views.guide.activate, name='guide_activate'),
    url(r'^guide/(?P<gid>\d+)/$', views.guide.profile, name='guide_profile'),
    url(r'^trip_filtering/', views.guide.FilterTrip.as_view(), name='filter_trip'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/$', views.guide.write_offer, name='write_offer'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/search_accom/$', views.guide.search_accom, name='search_accom'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/search_guide/$', views.guide.search_guide, name='search_guide'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/new_accom_form/$', views.guide.new_accom_form, name='new_accom_form'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/new_cost_form/$', views.guide.new_cost_form, name='new_cost_form'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/new_guide_form/$', views.guide.new_guide_form, name='new_guide_form'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/load_accom/$', views.guide.load_accom, name='load_accom'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/load_guide/$', views.guide.load_guide, name='load_guide'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/save_trans_offer/$', views.guide.save_trans_offer, name='save_trans_offer'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/save_accom_offer/$', views.guide.save_accom_offer, name='save_accom_offer'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/save_guide_offer/$', views.guide.save_guide_offer, name='save_guide_offer'),
    url(r'^guide/write_offer/(?P<req_id>\d+)/save_cost_offer/$', views.guide.save_cost_offer, name='save_cost_offer'),
    url(r'^upload_accom_photo/$', views.guide.upload_accom_photo, name='upload_accom_photo'),
    url(r'^upload_guide_photo/$', views.guide.upload_guide_photo, name='upload_guide_photo'),
    url(r'^save_accom_template/$', views.guide.save_accom_template, name='save_accom_template'),
    url(r'^save_guide_template/$', views.guide.save_guide_template, name='save_guide_template'),

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
