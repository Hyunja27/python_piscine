from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# from .models import Profile
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import HiddenInput, Textarea


# class CustomUserChangeForm(UserChangeForm):
#     password = None
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'first_name', 'last_name',]
        
# class ProfileForm(models.Model):
#     nickname = forms.CharField(label="별명", required=False)
#     description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())
#     image = forms.ImageField(label="이미지", required=False)
#        # 위의 내용을 정의하지 않아도 상관없지만, 화면에 출력될 때 label이 영문으로 출력되는 것이 싫어서 수정한 것이다..
#     class Meta:
#         model = Profile
#         fields = ['nickname', 'description', 'image',]

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",  "password1", "password2")

class FavoriteForm(forms.Form):
    article = forms.IntegerField(widget=HiddenInput(), required=True)

    def __init__(self, article, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if article is not None:
            self.fields['article'].initial = article

class PublishForm(forms.Form):
    title = forms.CharField(max_length=64, required=True)
    synopsis = forms.CharField(max_length=312, required=True)
    content = forms.CharField(widget=Textarea(), required=True)