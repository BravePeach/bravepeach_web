from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='이메일 주소',max_length=30,min_length=5,widget=forms.TextInput(attrs={'class' : 'regist-input'}))
    password = forms.CharField(label='비밀번호',widget=forms.PasswordInput(attrs={'class' : 'regist-input'}))


