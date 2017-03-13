from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.forms import extras

from .models import Profile


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


class GuideSearchForm(forms.Form):
    location = forms.CharField(max_length=200, label='')
    on_day = forms.CharField()
    traveler_cnt = forms.IntegerField()


# 회원정보 변경
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


class ProfileEditForm(forms.ModelForm):
    GENDER = (
        (1, "남성"),
        (2, "여성"),
    )

    birthday = forms.DateField(widget=extras.SelectDateWidget(years=range(1920, 2017),
                                                              attrs={"class": "input-select"},
                                                              empty_label=("년도*", "달*", "일*")))
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('birthday', 'gender')

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields["gender"].widget.attrs.update({"class": "input-radio"})


class PasswordResetCustomForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetCustomForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({"class": "input-text", "id": "reset-email"})


class SetPasswordCustcomForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordCustcomForm, self).__init__(*args, **kwargs)
        self.fields['new_passowrd1'].widget.attrs.update({"class": "input-text", "id": "new-password1"})
        self.fields['new_passowrd2'].widget.attrs.update({"class": "input-text", "id": "new-password2"})
