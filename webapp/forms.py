from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(max_length=30,min_length=5)
    password = forms.PasswordInput()
#   password = forms.CharField(widget=forms.PasswordInput)


