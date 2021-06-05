
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import HiddenInput

class Loginform(forms.Form):
    id = forms.CharField(required=True)
    pw = forms.CharField(required=True)

class TipForm(forms.Form):
    content = forms.CharField(required=True)

class DeleteTipForm(forms.Form):
    _method = forms.CharField(widget=HiddenInput(), initial='delete')
    id = forms.IntegerField(widget=HiddenInput())

    def __init__(self, id, *args, **kwargs):
        super(DeleteTipForm, self).__init__(*args, **kwargs)
        if id:
            self.fields['id'].initial = id

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",  "password1", "password2")

class VoteForm(forms.Form):
    _method = forms.CharField(widget=HiddenInput(), initial='put')
    id = forms.IntegerField(widget=HiddenInput())
    type = forms.BooleanField(required=False)
    def __init__(self, id, *args, **kwargs):
        super(VoteForm, self).__init__(auto_id='%s', *args, **kwargs)
        if id:
            self.fields['id'].initial = id

# class RegisterForm(forms.Form):
#     id = forms.CharField(min_length=6, max_length=32, required=True)
#     pw = forms.CharField(
#         widget=forms.PasswordInput, min_length=8, max_length=256, required=True)
#     pw_re = forms.CharField(
#         widget=forms.PasswordInput, min_length=8, max_length=256, required=True)
#     def clean(self):
#         data = self.cleaned_data
#         username = data.get("id")
#         password = data.get("pw")
#         confirm_password = data.get("pw_re")
#         # raise ValidationError('errrorrrr!!')
#         if password != confirm_password:
#             self.add_error('password', 'Passwords did not match')
#             self.add_error('confirm_password', 'Passwords did not match')
#         if UserData.objects.filter(username=username).exists():
#             self.add_error('username', "Already exist user name")
#         return self.cleaned_data