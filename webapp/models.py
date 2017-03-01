from django.db import models
# from django.contrib.auth.models import User
from hashid_field import HashidAutoField
from jsonfield import JSONField
# from django.utils import timezone


class User(models.Model):
    # 유저 고유 아이디는 해쉬함수로
    id = HashidAutoField(primary_key=True)
    pw = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=11, null=True)
    email = models.EmailField(max_length=50, null=True, unique=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    nationality = models.CharField(max_length=40, null=True)
    birthday = models.DateField()
    gender = models.BooleanField()
    # 디폴트 이미지 있어야함
    profile_image = models.URLField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    # delete_reason
    delete_reason_optional = models.CharField(max_length=100, null=True)
    is_guide = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    delete_reason = models.IntegerField(null= True)


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정한 시간 자동 저장되게 해야함
    modified_at = models.DateTimeField(null=True)


class Guide(models.Model):
    id = HashidAutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    pay_cnt = models.IntegerField(default=0)
    total_traveler_cnt = models.IntegerField(default=0)
    total_guide_day = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    guide_type = models.IntegerField(null=True)
    guide_theme = models.IntegerField(null=True)
    max_traveler_cnt = models.IntegerField(null=True)
    introduction = models.TextField(null=True)
    license = models.BooleanField(default=False)
    is_local = models.BooleanField(default=False)
    #기본값은 스루가이드
    activated = models.BooleanField(default=True)
    guide_location = JSONField(null=True)
    off_day = JSONField(null=True)
    career = JSONField(null=True)


class UserRequest(models.Model):
    city = JSONField
    travel_begin_at = models.DateField
    travel_end_at = models.DateField
    age_group = JSONField
    trans_type = models.IntegerField
    trans_via = models.IntegerField
    trans_class = models.IntegerField
    trans_comment = models.CharField(max_length=200)
    accom_location = models.IntegerField
    accom_location_optional = models.CharField(null=True, max_length=100)
    accom_type = models.IntegerField
    accom_comment = models.CharField(max_length=100)
    start_time = models.IntegerField
    end_time = models.IntegerField
    landmark = models.CharField(max_length=200)
    theme = models.IntegerField
    local_trans = models.CharField(max_length=200)
    guide_type = models.IntegerField
    importance = models.IntegerField
    cost = models.IntegerField
    published = models.BooleanField(default=False)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)


class Review(models.Model):
    # offer_id = models.ForeignKey('GuideOffer', on_delete=models.CASCADE)
    writer = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    content = models.TextField
    writer_id = models.IntegerField
    receiver_id = models.IntegerField
    location = models.CharField(max_length=100)


class GuideOffer(models.Model):
    paid = models.BooleanField(default=False)
    guide_id = models.ForeignKey('User', on_delete=models.CASCADE)
    request_id = models.ForeignKey('UserRequest', on_delete=models.CASCADE)
    etc = models.CharField(max_length=300)
    travel_period = JSONField
    trans_info = JSONField
    accom_template = JSONField
    guide_template = JSONField
    is_canceled = models.BooleanField(default=False)


class Like(models.Model):
    from_id = models.IntegerField
    to_id = models.IntegerField


class CancelledOffer(models.Model):
    offer_id = models.ForeignKey('GuideOffer', on_delete=models.CASCADE)
    user_id = models.IntegerField
    guide_id = models.IntegerField
    reason = models.CharField(max_length=500)


class AccomTemplate(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    map = models.CharField(max_length=200)
    content = models.TextField
    pic_list = JSONField
    guide_id = models.ForeignKey('Guide', on_delete=models.CASCADE)


class GuideTemplate(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField
    picture = models.CharField(max_length=200)
    guide_id = models.ForeignKey('Guide', on_delete=models.CASCADE)


class Cost(models.Model):
    type = models.IntegerField
    price = models.IntegerField
    info = models.CharField(max_length=100)
    offer_id = models.ForeignKey('GuideOffer', on_delete=models.CASCADE)

