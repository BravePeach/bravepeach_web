import math
from decimal import Decimal
import datetime

from django.db import models
from django_mysql.models import Model
from django.contrib.auth.models import User
from django_mysql.models import JSONField, ListCharField
from django.conf import settings
from redactor.fields import RedactorField

from bravepeach.const import GUIDE_THEME, GUIDE_TYPE


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_num = models.CharField(max_length=11, blank=True)
    is_guide = models.BooleanField(default=False)
    delete_reason = models.IntegerField(null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'))
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


class Guide(Model):
    # id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='guide')
    pay_cnt = models.IntegerField(default=0)
    total_traveler_cnt = models.IntegerField(default=0)
    total_guide_day = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'))
    guide_type = models.IntegerField(null=True, blank=True)
    guide_theme = models.IntegerField(null=True, blank=True)
    max_traveler_cnt = models.IntegerField(null=True, blank=True)
    introduction = models.TextField(blank=True)
    license = models.BooleanField(default=False)
    is_thru = models.BooleanField(default=False, verbose_name="스루 가이드")
    is_local = models.BooleanField(default=False, verbose_name="현지 가이드")   # 둘다 비어있으면 안됨
    activated = models.BooleanField(default=False)
    guide_location = JSONField(null=True, blank=True)
    off_day = JSONField(null=True, blank=True)
    career = JSONField(null=True, blank=True)
    real_name = models.TextField(null=False, blank=False, default="")
    certificate = JSONField(blank=True)
    appeal = JSONField(null=True, blank=True)
    essay = models.TextField(null=False, blank=False, default="")
    experience = JSONField(null=True, blank=True)
    is_volunteer = models.BooleanField(default=False)

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


class UserRequest(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    city = JSONField(null=True)
    travel_begin_at = models.DateField(null=True, blank=True)
    travel_end_at = models.DateField(null=True, blank=True)
    age_group = JSONField(null=True, blank=True)
    trans_type = models.IntegerField(default=0, blank=True)
    trans_via = models.IntegerField(default=0, blank=True)
    trans_class = models.IntegerField(default=0, blank=True)
    trans_comment = models.CharField(max_length=200, blank=True)
    accom_location = models.IntegerField(default=0, blank=True)
    accom_location_optional = models.CharField(null=True, max_length=100, blank=True)
    accom_type = models.IntegerField(default=0, blank=True)
    accom_comment = models.CharField(max_length=100, blank=True)
    start_time = models.IntegerField(default=0, blank=True)
    end_time = models.IntegerField(default=0, blank=True)
    landmark = models.CharField(max_length=200, blank=True)
    theme = models.IntegerField(default=0, blank=True)
    local_trans = models.IntegerField(default=0, blank=True)
    guide_type = models.IntegerField(default=0, blank=True)
    importance = models.IntegerField(default=0, blank=True)
    cost = models.IntegerField(default=0, blank=True)
    published = models.BooleanField(default=True, blank=True)
    additional_request = models.CharField(max_length=200, blank=True)

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
        options = ("직항", "경유 1회", "경유 2회")
        trans_via_list = [options[idx] for idx, v in enumerate(bin(self.trans_via)[2:]) if v == '1']
        return trans_via_list

    @property
    def trans_class_list(self):
        options = ("이코노미 석", "비즈니스 석", "퍼스트 석")
        trans_class_list = [options[idx] for idx, v in enumerate(bin(self.trans_class)[2:]) if v == '1']
        return trans_class_list

    @property
    def accom_locat_list(self):
        options = ("공항 근처", "시내", "여행지 근처", "기타")
        accom_locat_list = [options[idx] for idx, v in enumerate(bin(self.accom_location)[2:]) if v == '1']
        return accom_locat_list

    @property
    def accom_type_list(self):
        options = ("호텔", "한인 민박", "현지인 집", "리조트", "가이드 집")
        accom_type_list = [options[idx] for idx, v in enumerate(bin(self.accom_type)[2:]) if v == '1']
        return accom_type_list

    @property
    def theme_list(self):
        options = ("현지 꿀팁", "액티비티", "문화/예술", "골목 여행", "자연 경관", "맛집 기행", "역사여행")
        theme_list = [options[idx] for idx, v in enumerate(bin(self.theme)[2:]) if v == '1']
        return theme_list

    @property
    def local_trans_list(self):
        options = ("자동차", "대중교통", "자전거", "상관없음")
        local_trans_list = [options[idx] for idx, v in enumerate(bin(self.local_trans)[2:]) if v == '1']
        return local_trans_list

    @property
    def guide_type_list(self):
        options = ("유쾌한", "차분한", "지적인", "유머러스한", "감성적인", "설명을 잘하는", "경제적인")
        guide_type_list = [options[idx] for idx, v in enumerate(bin(self.guide_type)[2:]) if v == '1']
        return guide_type_list

    @property
    def importance_list(self):
        options = ("맛집", "인생사진", "적절한 휴식", "친구같은 가이드", "역사 공부", "기타")
        importance_list = [options[idx] for idx, v in enumerate(bin(self.importance)[2:]) if v == '1']
        return importance_list


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
    write_date = models.DateField(null=False, default=datetime.date.today())

    @property
    def clean_rating(self):
        frac_part, int_part = math.modf(self.rating)
        frac_part = 0 if frac_part < 0.5 else 0.5
        return range(int(int_part)), frac_part, range(4-int(int_part))


class Comment(Model):
    offer = models.ForeignKey(GuideOffer, related_name="comments")
    content = models.CharField(max_length=300, default="")
    writer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


# Guide2User
class GuideReview(Model):
    offer = models.ForeignKey(GuideOffer, related_name="guide_review")
    rating = models.FloatField(null=False)
    content = RedactorField(verbose_name="Content")
    writer = models.ForeignKey(Guide)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL)
    write_date = models.DateField(null=False, default=datetime.date.today())

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
