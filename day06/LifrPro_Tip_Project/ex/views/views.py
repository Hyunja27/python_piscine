from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from ..forms import RegisterForm
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import db
from django.shortcuts import render
from ..forms import TipForm, DeleteTipForm, VoteForm
from ..models import TipModel
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
        return redirect('index')


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
            return
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