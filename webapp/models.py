import math
from decimal import Decimal
import datetime

from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import JSONField, ListCharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from redactor.fields import RedactorField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_num = models.CharField(max_length=11, blank=True)
    is_guide = models.BooleanField(default=False)
    delete_reason = models.IntegerField(null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'))
    nationality = models.CharField(max_length=40, blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='profile/%Y_%m_%d', null=True)
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


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)


class Guide(models.Model):
    # id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    pay_cnt = models.IntegerField(default=0)
    total_traveler_cnt = models.IntegerField(default=0)
    total_guide_day = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'))
    guide_type = models.IntegerField(null=True, blank=True)
    guide_theme = models.IntegerField(null=True, blank=True)
    max_traveler_cnt = models.IntegerField(null=True, blank=True)
    introduction = models.TextField(blank=True)
    license = models.BooleanField(default=False)
    is_local = models.BooleanField(default=False)   # 기본값은 스루가이드
    activated = models.BooleanField(default=True)
    guide_location = JSONField(null=True, blank=True)
    off_day = JSONField(null=True, blank=True)
    career = JSONField(null=True, blank=True)

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
    def theme_list(self):
        theme_names = ("맛집", "역사", "골목")
        theme_lst = [theme_names[idx] for idx, v in enumerate(bin(self.guide_theme)[2:]) if v == '1']
        return theme_lst

    @property
    def style_list(self):
        style_names = ("quite", "noisy")
        style_lst = [style_names[idx] for idx, v in enumerate(bin(self.guide_type)[2:]) if v == '1']
        return style_lst


class UserRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    city = JSONField(null=True)
    travel_begin_at = models.DateField(null=True, blank=True)
    travel_end_at = models.DateField(null=True, blank=True)
    age_group = JSONField(null=True, blank=True)
    trans_type = models.IntegerField(null=True, blank=True)
    trans_via = models.IntegerField(null=True, blank=True)
    trans_class = models.IntegerField(null=True, blank=True)
    trans_comment = models.CharField(max_length=200, blank=True)
    accom_location = models.IntegerField(null=True, blank=True)
    accom_location_optional = models.CharField(null=True, max_length=100, blank=True)
    accom_type = models.IntegerField(null=True, blank=True)
    accom_comment = models.CharField(max_length=100, blank=True)
    start_time = models.IntegerField(null=True, blank=True)
    end_time = models.IntegerField(null=True, blank=True)
    landmark = models.CharField(max_length=200, blank=True)
    theme = models.IntegerField(null=True, blank=True)
    local_trans = models.CharField(max_length=200, blank=True)
    guide_type = models.IntegerField(null=True, blank=True)
    importance = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    published = models.BooleanField(default=True, blank=True)
    additional_request = models.CharField(max_length=200, blank=True)

    @property
    def trans_guided(self):
        if self.trans_via is None and self.trans_class is None and not self.trans_comment:
            return False
        return True

    @property
    def accom_guided(self):
        if self.accom_location is None and self.accom_type is None and not self.accom_comment:
            return False
        return True

    @property
    def guide_guided(self):
        if (self.start_time is None and self.end_time is None and not self.landmark and not self.theme and
                not self.guide_type and not self.importance):
            return False
        return True


class GuideOffer(models.Model):
    paid = models.BooleanField(default=False)
    guide = models.ForeignKey(Guide, related_name="offers")
    request = models.ForeignKey(UserRequest)
    etc = models.CharField(max_length=300, blank=True)
    travel_period = JSONField(null=True)
    trans_info = JSONField(null=True)
    accom_template = JSONField(null=True)
    guide_template = JSONField(null=True)
    is_canceled = models.BooleanField(default=False)


# User2Guide
class UserLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    guide = models.ForeignKey(Guide)


# Guide2User
class GuideLike(models.Model):
    guide = models.ForeignKey(Guide)
    request = models.ForeignKey(UserRequest)


class CancelledOffer(models.Model):
    offer = models.ForeignKey(GuideOffer, related_name="cancel")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    guide = models.IntegerField(null=True)
    reason = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)


class AccomTemplate(models.Model):
    title = models.CharField(max_length=100)
    # JSONField로 하려 했으나 migrate 과정에서 에러가 나서 일단은 ListField로..
    address = ListCharField(
        base_field=models.CharField(max_length=20),
        size=3,
        max_length=(3*21)
    )
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    content = models.TextField(blank=True)
    pic_list = JSONField(blank=True, null=True)
    guide = models.ForeignKey(Guide, related_name="accom_templates")
    type_id = models.IntegerField(default=0)

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
        type_list = ['호텔', '한인 민박', '현지인 집', '리조트', '가이드 집', '기타']
        return type_list[self.type_id]


class GuideTemplate(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    picture = models.CharField(max_length=200)
    guide = models.ForeignKey(Guide)


class Cost(models.Model):
    offer = models.ForeignKey(GuideOffer, related_name="costs")
    type_id = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    info = models.CharField(max_length=100)

    @property
    def type(self):
        type_list = ['이동수단', '숙소', '가이드비 / 수고비', '입장료 / 티켓값', '교통비', '식비', '기타']
        return type_list[self.type_id]


# User2Guide
class UserReview(models.Model):
    offer = models.ForeignKey(GuideOffer, related_name="user_review")
    rating = models.FloatField(null=False)
    content = RedactorField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    receiver = models.ForeignKey(Guide)
    write_date = models.DateField(null=False, default=datetime.date.today())

    @property
    def clean_rating(self):
        frac_part, int_part = math.modf(self.rating)
        frac_part = 0 if frac_part < 0.5 else 0.5
        return range(int(int_part)), frac_part, range(4-int(int_part))


class Comment(models.Model):
    offer = models.ForeignKey(GuideOffer, related_name="comments")
    content = models.CharField(max_length=300, default="")
    writer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


# Guide2User
class GuideReview(models.Model):
    offer = models.ForeignKey(GuideOffer, related_name="guide_review")
    rating = models.FloatField(null=False)
    content = RedactorField()
    writer = models.ForeignKey(Guide)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL)
    write_date = models.DateField(null=False, default=datetime.date.today())

    @property
    def clean_rating(self):
        frac_part, int_part = math.modf(self.rating)
        frac_part = 0 if frac_part < 0.5 else 0.5
        return range(int(int_part)), frac_part, range(4-int(int_part))
