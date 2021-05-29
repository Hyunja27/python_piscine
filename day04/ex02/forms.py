from django import forms

class MsForm(forms.Form):
    initial = {'Your_ms': 'Sherlock'}
    your_ms = forms.CharField(label='모든 피시너들에게! 응원의 한마디 해주세요!', max_length=20)