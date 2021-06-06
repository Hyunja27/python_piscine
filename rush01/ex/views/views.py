from typing import Any
from django.db.utils import DatabaseError
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, DetailView
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import db
from django.shortcuts import render
from rush01 import settings
from django.conf.urls.static import static

from ex.forms import TipForm, DeleteTipForm, VoteForm, CustomUserChangeForm, ProfileForm, RegisterForm
from ex.models import TipModel, Profile
from django.urls import reverse_lazy

class Index(View):
    template_name = "index.html"

    def get(self, request):
        try:
            tips = TipModel.objects.all().order_by('-date')

        except db.DatabaseError as e:
            tips = []
        context = {
            'tipform': TipForm(),
            'tips': [{
                'id': tip.id,
                'content': tip.content,
                'author': tip.author,
                'date': tip.date,
                'up_votes': tip.up_votes,
                'down_votes': tip.down_votes,
                'deleteform': DeleteTipForm(tip.id),
                'voteform': VoteForm(tip.id),
            } for tip in tips],
        }
        print([(tip.up_votes.count(), tip.down_votes.count()) for tip in tips])
        return render(request, self.template_name, context)


class Logout(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect('login')


class Show_Page(View):
    template_name = "mainpage.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class Register(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already logined!')
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: RegisterForm):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful registration. Invalid information.")
        return super().form_invalid(form)

class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already logined!')
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: AuthenticationForm):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            messages.error(self.request, "Invalid username or password.")
            return super().form_invalid(form)
        login(self.request, user)
        messages.info(self.request, f"You are now logged in as {username}.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Tip(LoginRequiredMixin, View):
    http_method_names = ['post', 'put', 'delete']
    login_url = reverse_lazy('login')

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(Tip, self).dispatch(*args, **kwargs)

    def post(self, request):
        form = TipForm(request.POST)
        if form.is_valid():
            try:
                TipModel.objects.create(
                    content=form.cleaned_data['content'],
                    author=self.request.user
                )
                messages.success(self.request, "Successful create Tip.")
            except DatabaseError as e:
                print(e)
                messages.error(
                    self.request, "Unsuccessful create Tip. (db error)")
        else:
            messages.error(
                self.request, "Unsuccessful create Tip. (Invalid form data.)")
        return redirect('index')

    def __error_msg(self, method, msg):
        messages.error(
            self.request, f"Unsuccessful {method} Tip. ({msg})")
        return redirect('index')

    def delete(self, request: HttpRequest):
        form = DeleteTipForm(None, request.POST)
        if not form.is_valid():
            return self.__error_msg("delete", "Invaild form data.")
        try:
            tip: TipModel = TipModel.objects.get(
                id=form.cleaned_data['id'])
            if tip.author != request.user and request.user.is_staff == False and request.user.is_superuser == False:
                return self.__error_msg("delete", "access denied")
            tip.delete()
            messages.success(self.request, "Successful Erase Tip.")
        except TipModel.DoesNotExist as e:
            return self.__error_msg("delete", "Tip does not exist")
        except DatabaseError as e:
            return self.__error_msg("delete", "db error")

        return redirect('index')

    def put(self, request):
        form = VoteForm(None, request.POST)
        if not form.is_valid():
            return self.__error_msg("vote", "Invaild form data.")
        try:
            tip: TipModel = TipModel.objects.get(id=form.cleaned_data['id'])
            if form.cleaned_data['type']:
                tip.upvote(request.user)
            elif tip.author != request.user and request.user.groups.filter(name='NoNo').exists():
                return self.__error_msg("vote", "Oh... You are a NoNo User! No!!")
            else:
                tip.downvote(request.user)
        except TipModel.DoesNotExist as e:
            return self.__error_msg("vote", "Tip does not exist")
        except DatabaseError as e:
            return self.__error_msg("vote", "db error")
        messages.success(request, 'Dood Voted!')
        return redirect('index')


def Profile_Edit(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm("12345", "6789", "image_hahehihoho", request.POST, request.FILES, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('index')
        return redirect('profile')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm("12345", "6789", "image_hahehihoho",instance=profile)
        return render(request, 'profile.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form
        })

class Detail_View(DetailView):
    template_name = 'detail.html'
    model = TipForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = TipForm
        return context

def Admin_edit(request):
    return redirect('admin')
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm("12345", "6789", "image_hahehihoho", request.POST, request.FILES, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('index')
        return redirect('profile')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm("12345", "6789", "image_hahehihoho",instance=profile)
        return render(request, 'profile.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form
        })