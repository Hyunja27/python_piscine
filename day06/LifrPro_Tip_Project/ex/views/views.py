from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from ..forms import RegisterForm
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import db
from django.shortcuts import render
from ..forms import TipForm
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
            'tips': tips
        }
        return render(request, self.template_name, context)

class Logout(LoginRequiredMixin, View):
    success_url = reverse_lazy('index')

    def get(self, request):
        messages.info(request, "You have successfully logged out.")
        request.session.flush()
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
                messages.error(
                    self.request, "Unsuccessful create Tip. (db error)")
        else:
            messages.error(
                self.request, "Unsuccessful create Tip. (Invalid form data.)")
        return redirect('index')