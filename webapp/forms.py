from django import forms

class GuideSearch(forms.Form):
    traveler_cnt = forms.IntegerField(label='traveler_cnt')

