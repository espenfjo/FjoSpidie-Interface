from django import forms

class JobForm(forms.Form):
    url       = forms.CharField()
    useragent = forms.CharField(required=False)
    referer   = forms.CharField(required=False)
