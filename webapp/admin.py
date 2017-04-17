from django.contrib import admin
from django.db import models

from .models import (Profile, Guide, UserRequest, GuideOffer, AccomTemplate, GuideTemplate, CancelledOffer,
                     UserReview, GuideReview, Notice, GuideAdjust, UserAlarm, GuideAlarm, Cost, Journal,
                     UserPost, UserPostHit)

from redactor.widgets import RedactorEditor


class ProfileAdmin(admin.ModelAdmin):
    # list_display = ['user', 'birthday', 'photo']
    pass


class GuideAdmin(admin.ModelAdmin):
    pass


class UserRequestAdmin(admin.ModelAdmin):
    pass


class GuideOfferAdmin(admin.ModelAdmin):
    pass


class AccomTemplateAdmin(admin.ModelAdmin):
    pass


class GuideTemplateAdmin(admin.ModelAdmin):
    pass


class CostAdmin(admin.ModelAdmin):
    pass


class CancelledOfferAdmin(admin.ModelAdmin):
    pass


class UserReviewAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": RedactorEditor}
    }


class GuideReviewAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": RedactorEditor}
    }


class NoticeAdmin(admin.ModelAdmin):
    pass


class GuideAdjustAdmin(admin.ModelAdmin):
    pass


class JournalAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": RedactorEditor}
    }


class UserAlarmAdmin(admin.ModelAdmin):
    pass


class GuideAlarmAdmin(admin.ModelAdmin):
    pass


class UserPostAdmin(admin.ModelAdmin):
    pass


class UserPostHitAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Guide, GuideAdmin)
admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(GuideOffer, GuideOfferAdmin)
admin.site.register(AccomTemplate, AccomTemplateAdmin)
admin.site.register(GuideTemplate, GuideTemplateAdmin)
admin.site.register(Cost, CostAdmin)
admin.site.register(CancelledOffer, CancelledOfferAdmin)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(GuideReview, GuideReviewAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(UserAlarm, UserAlarmAdmin)
admin.site.register(GuideAlarm, GuideAlarmAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(UserPostHit, UserPostHitAdmin)
