from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=11, null=True)
    is_guide = models.BooleanField(default=False)
    delete_reason = models.IntegerField(null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    nationality = models.CharField(max_length=40, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.NullBooleanField(null=True)
    # profile_image = models.URLField(default='',  null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    deleted_at = models.DateTimeField(null=True)
    delete_reason_optional = models.CharField(max_length=100, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정한 시간 자동 저장되게 해야함
    modified_at = models.DateTimeField(null=True)


class Guide(models.Model):
    # id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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


class GuideOffer(models.Model):
    paid = models.BooleanField(default=False)
    guide = models.ForeignKey(Guide)
    request = models.ForeignKey(UserRequest)
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
    offer = models.ForeignKey(GuideOffer)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    guide = models.IntegerField
    reason = models.CharField(max_length=500)


class AccomTemplate(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    map = models.CharField(max_length=200)
    content = models.TextField
    pic_list = JSONField
    guide = models.ForeignKey(Guide)


class GuideTemplate(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField
    picture = models.CharField(max_length=200)
    guide = models.ForeignKey(Guide)


class Cost(models.Model):
    type = models.IntegerField
    price = models.IntegerField
    info = models.CharField(max_length=100)
    offer = models.ForeignKey(GuideOffer)


class Review(models.Model):
    offer = models.ForeignKey(GuideOffer)
    writer = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    content = models.TextField
    writer_id = models.IntegerField
    receiver_id = models.IntegerField
    location = models.CharField(max_length=100)
