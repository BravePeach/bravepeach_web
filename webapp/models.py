import math
import datetime
import json

from channels import Group
from django.utils import timezone
from django.db import models
from django_mysql.models import Model
from django.contrib.auth.models import User
from django_mysql.models import JSONField, ListCharField
from django.conf import settings
from redactor.fields import RedactorField

from bravepeach.const import *
from bravepeach.settings import MSG_TYPE_MESSAGE


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fb_id = models.CharField(max_length=200, null=True, blank=True)
    ggl_id = models.CharField(max_length=200, null=True, blank=True)
    naver_id = models.CharField(max_length=200, null=True, blank=True)
    phone_num = models.CharField(max_length=11, blank=True)
    is_guide = models.BooleanField(default=False)
    delete_reason = models.IntegerField(null=True)
    rating = models.FloatField(default=0.0)
    nationality = models.CharField(max_length=40, blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='profile/%Y_%m_%d', default='profile/2017_03_22/2__15_12_33_307511.jpg')
    deleted_at = models.DateTimeField(null=True)
    delete_reason_optional = models.CharField(max_length=100, blank=True)
    mail_certified = models.BooleanField(default=False)
    phone_certified = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile for user dict'.format(self.user.username)

    @property
    def full_name(self):
        if all(ord(char) < 128 for char in self.user.last_name+self.user.first_name):
            return " ".join([self.user.first_name, self.user.last_name])
        else:
            return "".join([self.user.last_name, self.user.first_name])

    @property
    def is_volunteer(self):
        vol = self.user.volunteer.all()
        if len(vol) == 0:
            return False
        return True


class Notice(Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class Guide(Model):
    # id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='guide')
    pay_cnt = models.IntegerField(default=0)
    total_traveler_cnt = models.IntegerField(default=0)
    total_guide_day = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    guide_type = models.IntegerField(null=True, blank=True)
    guide_theme = models.IntegerField(null=True, blank=True)
    max_traveler_cnt = models.IntegerField(null=True, blank=True)
    introduction = models.TextField(blank=True)
    license = models.BooleanField(default=False)
    is_thru = models.BooleanField(default=False, verbose_name="스루 가이드")
    is_local = models.BooleanField(default=False, verbose_name="현지 가이드")   # 둘다 비어있으면 안됨
    activated = models.BooleanField(default=True)
    guide_location = JSONField(null=True, blank=True)
    guide_country = JSONField(null=True, blank=True)
    guide_city = JSONField(null=True, blank=True)
    off_day = JSONField(null=True, blank=True)
    career = JSONField(null=True, blank=True)
    real_name = models.TextField(null=False, blank=False, default="")
    certificate = JSONField(blank=True)
    appeal = JSONField(null=True, blank=True)
    essay = models.TextField(null=False, blank=False, default="")
    experience = JSONField(null=True, blank=True)
    is_volunteer = models.BooleanField(default=False)

    def __str__(self):
        return "Guide: {}".format(self.full_name)

    @property
    def full_name(self):
        if all(ord(char) < 128 for char in self.user.last_name+self.user.first_name):
            return " ".join([self.user.first_name, self.user.last_name])
        else:
            return "".join([self.user.last_name, self.user.first_name])

    @property
    def clean_rating(self):
        frac_part, int_part = math.modf(self.rating)
        frac_part = 0 if frac_part < 0.5 else 0.5
        return range(int(int_part)), frac_part, range(4-int(int_part))

    @property
    def guide_cnt(self):
        return len(self.offers.filter(paid=True, is_canceled=False,
                                      request__travel_end_at__lt=datetime.date.today()))

    @property
    def review_cnt(self):
        return UserReview.objects.filter(receiver=self.id).count()

    @property
    def theme_list(self):
        lst = [v for k, v in GUIDE_THEME if self.guide_type & k == k]
        print(lst)
        return lst
        # theme_names = (x[1] for x in GUIDE_THEME)
        # theme_lst = [theme_names[idx] for idx, v in enumerate(bin(self.guide_theme)[2:]) if v == '1']
        # return theme_lst

    @property
    def style_list(self):
        lst = [v for k, v in GUIDE_TYPE if self.guide_type & k == k]
        return lst
        # style_names = (x[1] for x in GUIDE_TYPE)
        # print(bin(self.guide_type)[2:])
        # style_lst = [style_names[idx] for idx, v in enumerate(bin(self.guide_type)[2:]) if v == '1']
        # return style_lst


class GuideAdjust(Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='adjust')
    name = models.TextField(null=False, blank=False, verbose_name="수취인 이름*")
    bank = models.TextField(null=False, blank=False, verbose_name="은행 이름*")
    account_num = models.TextField(null=False, blank=False, verbose_name="계좌번호 (유럽은행의 경우 IBAN CODE를 적어주세요)*")
    swift_bic_code = models.TextField(null=False, blank=True, default="", verbose_name="SWIFT BIC CODE (해외 계좌일 경우)")
    branch = models.TextField(null=False, blank=True, default="", verbose_name="은행 지점명 (해외 계좌일 경우)")
    addr = models.TextField(null=False, blank=True, default="", verbose_name="수취인 주소 (해외 계좌일 경우)")
    routing_num = models.TextField(null=False, blank=True, default="", verbose_name="Routing Number (미국 은행일 경우)")

    def __str__(self):
        return "{}'s Adjust".format(self.guide.full_name)


class UserRequest(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    city = JSONField(null=True)
    # 도시이름으로 검색할때 city 필드의 정보만으로는 부족하여
    # 여행자가 입력한 도시의 국가와 최상위 도시를 저장하는 필드들
    countries = JSONField(null=True, blank=True)
    cities = JSONField(null=True, blank=True)
    travel_begin_at = models.DateField(null=True, blank=True)
    travel_end_at = models.DateField(null=True, blank=True)
    age_group = JSONField(null=True, blank=True)
    trans_type = models.IntegerField(default=0, blank=True)
    trans_start_at = models.IntegerField(default=0, blank=True)
    trans_arrive_at = models.IntegerField(default=0, blank=True)
    trans_via = models.IntegerField(default=0, blank=True)
    trans_class = models.IntegerField(default=0, blank=True)
    trans_comment = models.CharField(max_length=200, blank=True)
    accom_location = models.IntegerField(default=0, blank=True)
    accom_location_optional = models.CharField(default="", max_length=100, blank=True)
    accom_type = models.IntegerField(default=0, blank=True)
    accom_comment = models.CharField(max_length=100, blank=True)
    start_time = models.IntegerField(default=0, blank=True)
    end_time = models.IntegerField(default=0, blank=True)
    landmark = models.CharField(max_length=200, blank=True, default="")
    theme = models.IntegerField(default=0, blank=True)
    local_trans = models.IntegerField(default=0, blank=True)
    guide_major = models.IntegerField(default=0, blank=True)
    guide_type = models.IntegerField(default=0, blank=True)
    importance = models.IntegerField(default=0, blank=True)
    importance_optional = models.CharField(default="", max_length=100, blank=True)
    cost = models.IntegerField(default=0, blank=True)
    published = models.BooleanField(default=True, blank=True)
    additional_request = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{}'s request // {} ~ {} to {}".format(self.user.profile.full_name, self.travel_begin_at, self.travel_end_at, self.city)

    @property
    def trans_guided(self):
        if not self.trans_via and not self.trans_class and not self.trans_comment:
            return False
        return True

    @property
    def accom_guided(self):
        if not self.accom_location and not self.accom_type and not self.accom_comment:
            return False
        return True

    @property
    def guide_guided(self):
        if (self.start_time == 1 and self.end_time == 1 and not self.landmark and not self.theme and
                not self.guide_type and not self.importance):
            return False
        return True

    @property
    def total_traveler(self):
        return sum(self.age_group)

    @property
    def toddler_traveler(self):
        return self.age_group[0]

    @property
    def child_traveler(self):
        return self.age_group[1]

    @property
    def adult_traveler(self):
        return sum(self.age_group[2:])

    @property
    def trans_via_list(self):
        lst = [v for k, v in TRANS_VIA if self.trans_via & k == k]
        return lst

    @property
    def trans_class_list(self):
        lst = [v for k, v in TRANS_CLASS if self.trans_class & k == k]
        return lst

    @property
    def accom_locat_list(self):
        lst = [v for k, v in ACCOM_LOCATION if self.accom_location & k == k]
        return lst

    @property
    def accom_type_list(self):
        lst = [v for k, v in ACCOM_TYPE if self.accom_type & k == k]
        return lst

    @property
    def theme_list(self):
        lst = [v for k, v in THEME if self.theme & k == k]
        return lst

    @property
    def local_trans_list(self):
        lst = [v for k, v in LOCAL_TRANS if self.local_trans & k == k]
        return lst

    @property
    def guide_type_list(self):
        lst = [v for k, v in GUIDE_TYPE if self.guide_type & k == k]
        return lst

    @property
    def importance_list(self):
        lst = [v for k, v in IMPORTANCE if self.importance & k == k]
        return lst

    @property
    def guide_major_list(self):
        lst = [v for k, v in GUIDE_MAJOR if self.guide_major & k == k]
        return lst


class GuideOffer(Model):
    paid = models.BooleanField(default=False)
    guide = models.ForeignKey(Guide, related_name="offers")
    request = models.ForeignKey(UserRequest)
    etc = models.CharField(max_length=300, blank=True)
    travel_period = JSONField(null=True)
    trans_info = models.CharField(max_length=500)
    accom_template = JSONField(null=True)
    guide_template = JSONField(null=True)
    is_canceled = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    adjust_requested_at = models.DateField(null=True)
    adjust_done_at = models.DateField(null=True)

    def __str__(self):
        return "{}'s offer to req #{}".format(self.guide.full_name, self.request.id)

    @property
    def total_cost(self):
        return sum([x.price for x in self.costs.all() if x.type_id != 2]) + self.guide_cost()

    def guide_cost(self):
        return int(sum([x.price for x in self.costs.all() if x.type_id == 2]) * 0.12)


# User2Guide
class UserLike(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    guide = models.ForeignKey(Guide)


# Guide2User
class GuideLike(Model):
    guide = models.ForeignKey(Guide)
    request = models.ForeignKey(UserRequest)


class CancelledOffer(Model):
    offer = models.ForeignKey(GuideOffer, related_name="cancel")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    guide = models.IntegerField(null=True)
    reason = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)


class AccomTemplate(Model):
    title = models.CharField(max_length=100)
    # JSONField로 하려 했으나 migrate 과정에서 에러가 나서 일단은 ListField로..
    # 견적서 상세보기 페이지에서 숙소에 대한 위치를 국가, 시, 구 정도까지 보여주는데 그 주소를 저장하기 위한 필드입니다.
    address = ListCharField(
        base_field=models.CharField(max_length=20),
        size=3,
        max_length=(3*21)
    )
    # 위도와 경도를 저장하는 필드입니다.
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    content = models.TextField(blank=True)
    guide = models.ForeignKey(Guide, related_name="accom_templates")
    type_id = models.IntegerField(default=0)
    overwritten = models.BooleanField(default=False)

    @property
    def country(self):
        return self.address[0]

    @property
    def city(self):
        return self.address[1]

    @property
    def small_city(self):
        return self.address[2]

    @property
    def type(self):
        type_list = ['기타', '호텔', '한인 민박', '현지인 집', '리조트', '가이드 집']
        return type_list[self.type_id]


class AccomPhoto(Model):
    accom_template = models.ForeignKey(AccomTemplate, related_name="accom_photos")
    photo = models.ImageField(upload_to='accom_photos/%Y_%m_%d')


class GuideTemplate(Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='guide_photos/%Y/%m/%d')
    guide = models.ForeignKey(Guide, related_name="guide_templates")
    overwritten = models.BooleanField(default=False)


class Cost(Model):
    offer = models.ForeignKey(GuideOffer, related_name="costs")
    type_id = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    info = models.CharField(max_length=100)

    @property
    def type(self):
        type_list = ['이동수단', '숙소', '가이드비 / 수고비', '입장료 / 티켓값', '교통비', '식비', '기타']
        return type_list[self.type_id]


# User2Guide
class UserReview(Model):
    offer = models.ForeignKey(GuideOffer, related_name="user_review")
    rating = models.FloatField(null=False)
    content = RedactorField(verbose_name=u'Content')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    receiver = models.ForeignKey(Guide)
    write_date = models.DateField(null=False, default=timezone.now)

    def __str__(self):
        # return "Review from {} to {} for travel(offer) {}".format(self.writer.profile.full_name,
        #                                                           self.receiver.full_name, self.offer.id)
        return "Review from {} to {} for travel(offer) #{}".format(self.writer.profile.full_name,
                                                                   self.receiver.full_name, self.offer.id)

    @property
    def clean_rating(self):
        frac_part, int_part = math.modf(self.rating)
        frac_part = 0 if frac_part < 0.5 else 0.5
        return range(int(int_part)), frac_part, range(4-int(int_part))


# Guide2User
class GuideReview(Model):
    offer = models.ForeignKey(GuideOffer, related_name="guide_review")
    rating = models.FloatField(null=False)
    content = RedactorField(verbose_name="Content")
    writer = models.ForeignKey(Guide)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL)
    write_date = models.DateField(null=False, default=timezone.now)

    def __str__(self):
        return "Review from {} to {} for travel #{}".format(self.writer.full_name,
                                                            self.receiver.profile.full_name,
                                                            self.offer_id)

    @property
    def clean_rating(self):
        frac_part, int_part = math.modf(self.rating)
        frac_part = 0 if frac_part < 0.5 else 0.5
        return range(int(int_part)), frac_part, range(4-int(int_part))


class Journal(Model):
    offer = models.ForeignKey(GuideOffer, related_name='journal')
    thumbnail = models.ImageField(upload_to='journal/%Y_%m_%d')
    content = RedactorField(verbose_name="Content")
    writer = models.ForeignKey(Guide)
    write_date = models.DateField(null=False)

    def __str__(self):
        return "{}'s Journal for travel #{}".format(self.writer.full_name, self.offer_id)


class UserAlarm(Model):
    # sender = models.ForeignKey(Guide)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='alarms')
    contents = models.CharField(max_length=200, null=False, blank=False)
    landing = models.CharField(max_length=100, null=True)
    immediate = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return "User Alarm to {}".format(self.receiver.profile.full_name)


class GuideAlarm(Model):
    # sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    receiver = models.ForeignKey(Guide, related_name='alarms')
    contents = models.CharField(max_length=200, null=False, blank=False)
    landing = models.CharField(max_length=100, null=True, blank=True)
    immediate = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return "Guide Alarm to {}".format(self.receiver.full_name)


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )


class UserPost(Model):
    writer = models.ForeignKey(User, related_name="post")
    title = models.CharField(max_length=50, default="")
    content = RedactorField(verbose_name=u'Content')
    written_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}'s post".format(self.writer.profile.full_name)


class UserPostHit(Model):
    post = models.ForeignKey(UserPost, related_name="user_post_hit")
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Hit {}'s post with session key: {}".format(self.post.writer.profile.full_name, self.session)


class UserComment(Model):
    post = models.ForeignKey(UserPost, related_name="user_comment")
    content = models.CharField(max_length=300, default="")
    writer = models.ForeignKey(User, related_name="user_comment")
    written_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}'s comment to post {}".format(self.writer.profile.full_name, self.post.id)
