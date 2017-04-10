import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.forms import extras

from .models import (Profile, UserRequest, UserReview, GuideOffer, AccomTemplate, GuideTemplate, Guide, GuideAdjust,
                     GuideReview, Journal)
from redactor.widgets import RedactorEditor


class LoginForm(forms.Form):
    email = forms.CharField(label='이메일 주소', max_length=30, min_length=5,
                            widget=forms.TextInput(attrs={'class': 'input-text'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'input-text'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].widget.attrs.update({"class": "input-text", "placeholder": "성(Last Name)*",
                                                      "required": "true"})
        self.fields['first_name'].widget.attrs.update({"class": "input-text", "placeholder": "이름(First Name)*",
                                                       "required": "true"})
        self.fields['password'].widget.attrs.update({"class": "input-text", "placeholder": "비밀번호*"})
        self.fields['password2'].widget.attrs.update({"class": "input-text", "placeholder": "비밀번호 확인*"})
        self.fields['email'].widget.attrs.update({"class": "input-text", "placeholder": "이메일(E-mail)*"})

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


# 회원정보 변경
class UserEditForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({"class": "input-text", "placeholder": "비밀번호*"})
        self.fields['password2'].widget.attrs.update({"class": "input-text", "placeholder": "비밀번호 확인*"})
        self.fields['email'].widget.attrs.update({"class": "input-text", "placeholder": "이메일(E-mail)*",
                                                  "readonly": True})


class ProfileEditForm(forms.ModelForm):
    GENDER = (
        (1, "남성"),
        (2, "여성"),
    )

    birthday = forms.DateField(widget=extras.SelectDateWidget(years=range(1920, datetime.date.today().year),
                                                              attrs={"class": "input-select"},
                                                              empty_label=("년도*", "달*", "일*")))
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('birthday', 'gender')

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields["gender"].widget.attrs.update({"class": "input-radio"})


class UnsubscribeForm(forms.ModelForm):
    DELETE_REASON_LIST = (
        (1, "앞으로 여행갈 일이 없을 것 같습니다."),
        (2, "다른 BravePeach 계정이 있습니다."),
        (3, "BravePeach가 유용하지 않습니다."),
        (4, "가이드와 불화로 인해 BravePeach를 탈퇴하고 싶습니다."),
        (5, "BravePeach가 보내는 이메일, 초대, 요청이 너무 많습니다."),
        (6, "BravePeach가 안전하지 않다고 생각합니다."),
        (7, "내 계정이 해킹당했습니다."),
        (8, "개인정보가 우려됩니다."),
        (9, "BravePeach에 너무 많은 시간을 사용합니다."),
        (10, "기타 내용은 자세히 설명해주세요."),
    )

    delete_reason = forms.ChoiceField(choices=DELETE_REASON_LIST, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('delete_reason', 'delete_reason_optional',)

    def __init__(self, *args, **kwargs):
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        self.fields['delete_reason'].widget.attrs.update({"class": "input-radio"})
        self.fields["delete_reason_optional"].widget.attrs.update({"class": "input-textarea",
                                                                   "placeholder": "이유를 직접 적어주세요 (200자 이내)"})


class PasswordResetCustomForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetCustomForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({"class": "input-text", "id": "reset-email"})


class RequestForm(forms.ModelForm):
    travel_begin_at = forms.DateField(input_formats=['%Y.%m.%d'], required=False)
    travel_end_at = forms.DateField(input_formats=['%Y.%m.%d'], required=False)
    trans_start_at = forms.ChoiceField(choices=((i, i) for i in range(1, 25)))
    trans_arrive_at = forms.ChoiceField(choices=((i, i) for i in range(1, 25)))
    start_time = forms.ChoiceField(choices=((i, i) for i in range(1, 25)))
    end_time = forms.ChoiceField(choices=((i, i) for i in range(1, 25)))
    cost = forms.NumberInput
    city = forms.CharField(initial="")
    age_group = forms.CharField(initial="")

    class Meta:
        model = UserRequest
        fields = [
            'user', 'city', 'travel_begin_at', 'travel_end_at', 'trans_start_at', 'trans_arrive_at', 'age_group', 'trans_type', 'trans_via', 'trans_class',
            'trans_comment', 'accom_location', 'accom_location_optional', 'accom_type', 'accom_comment',
            'start_time', 'end_time', 'landmark', 'theme', 'local_trans', 'guide_type', 'importance', 'cost',
            'additional_request', 'accom_location_optional', 'importance_optional', 'guide_major'
        ]
        widgets = {
            'trans_comment': forms.Textarea,
            'accom_comment': forms.Textarea,
            'additional_request': forms.Textarea,
            'user': forms.HiddenInput,
        }


class GuideSearchFrom(forms.Form):
    city = forms.CharField(widget=forms.TextInput, required=False)
    travel_begin_at = forms.DateField(input_formats=['%Y.%m.%d'], required=False)
    travel_end_at = forms.DateField(input_formats=['%Y.%m.%d'], required=False)
    age_group = forms.CharField(widget=forms.TextInput, required=False)


class SetPasswordCustcomForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordCustcomForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({"class": "input-text", "id": "new-password1"})
        self.fields['new_password2'].widget.attrs.update({"class": "input-text", "id": "new-password2"})


class UserReviewForm(forms.ModelForm):
    # content = forms.CharField(widget=RedactorEditor)

    class Meta:
        model = UserReview
        fields = ('rating', 'content')
        widgets = {'content': RedactorEditor}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget.attrs.update({"class": "hidden"})


class WriteOfferForm(forms.ModelForm):
    class Meta:
        model = GuideOffer
        fields = ['trans_info', 'accom_template', 'guide_template']


class VolunteerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['real_name'].widget.attrs.update({"class": "input-text", "placeholder": "실명"})
        self.fields['essay'].widget.attrs.update({"class": "input-textarea", "placeholder": "BravePeach에서 진행하고 싶은 여행 혹은 원하는 여행자에 대해서 적어주세요."})
        self.fields['is_thru'].widget.attrs.update({"class": "input-checkbox"})
        self.fields['is_local'].widget.attrs.update({"class": "input-checkbox"})
        self.fields['introduction'].widget.attrs.update({"class": "input-textarea", "placeholder": "자기소개"})

    class Meta:
        model = Guide
        fields = ["real_name", "is_thru", "is_local", "guide_location", "guide_country", "guide_city", "introduction",
                  "career", "certificate", "appeal", "guide_type", "guide_theme", "essay", "experience"]


class GuideAdjustForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "input-text", "placeholder": f.label})

    class Meta:
        model = GuideAdjust
        fields = ['name', 'bank', 'account_num', 'swift_bic_code', 'branch', 'addr', 'routing_num']


class GuideReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget.attrs.update({"class": "hidden"})

    class Meta:
        model = GuideReview
        fields = ['rating', 'content']
        widgets = {'content': RedactorEditor}


class JournalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thumbnail'].widget.attrs.update({"class": "hidden"})

    class Meta:
        model = Journal
        fields = ['thumbnail', 'content']
        widgets = {'content': RedactorEditor}
