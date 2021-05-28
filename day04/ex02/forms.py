from django import forms

class MsForm(forms.Form):
    your_ms = forms.CharField(label='Your message', max_length=20)