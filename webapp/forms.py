from django import forms
from django.contrib.auth.models import User
from .models import Profile, UserRequest
from django.forms import extras


class LoginForm(forms.Form):
    email = forms.CharField(label='이메일 주소',max_length=30,min_length=5,widget=forms.TextInput(attrs={'class' : 'regist-input'}))
    password = forms.CharField(label='비밀번호',widget=forms.PasswordInput(attrs={'class' : 'regist-input'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


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

    birthday = forms.DateField(widget=extras.SelectDateWidget(years=range(1950, 2017)))
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('photo', 'phone_num', 'nationality')


# 요청서 작성
class RequestForm(forms.ModelForm):
    travel_begin_at = forms.DateField(input_formats=['%Y.%m.%d'], required=False)
    travel_end_at = forms.DateField(input_formats=['%Y.%m.%d'], required=False)
    CHOICES1 = ((i, i) for i in range(1, 25))
    CHOICES2 = ((i, i) for i in range(1, 25))
    start_time = forms.ChoiceField(choices=CHOICES1)
    end_time = forms.ChoiceField(choices=CHOICES2)
    cost = forms.NumberInput

    class Meta:
        model = UserRequest
        fields = [
            'city', 'travel_begin_at', 'travel_end_at', 'age_group', 'trans_type', 'trans_via', 'trans_class',
            'trans_comment', 'accom_location', 'accom_location_optional', 'accom_type', 'accom_comment',
            'start_time', 'end_time', 'landmark', 'theme', 'local_trans', 'guide_type', 'importance', 'cost', 'additional_request'
        ]
        widgets = {
            'city': forms.TextInput,
            'age_group': forms.TextInput,
            'trans_comment': forms.Textarea,
            'accom_comment': forms.Textarea,
            'additional_request': forms.Textarea,
        }

