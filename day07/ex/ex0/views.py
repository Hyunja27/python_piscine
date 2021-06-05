from typing import Any
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import RedirectView
from django.views.generic import ListView, DetailView
from .models import Article, UserFavoriteArticle
from django.views import View
from .form import RegisterForm, FavoriteForm, PublishForm
from django.db import DatabaseError

# Create your views here.

# class Index():


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect('home')

class HomeView(RedirectView):
    pattern_name = 'article'


class ArticleView(ListView):
    template_name = 'index.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PublicView(ListView):
    template_name = 'index.html'
    model = Article
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

class FavoriteView(DetailView):
    template_name = 'favorite.html'
    model = Article

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class Register_View(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Already log on!')
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: RegisterForm) -> HttpResponse:
        login(self.request, form.save())
        messages.success(self.request, 'Wellcome!')
        return super().form_valid(form)
    
    def form_invalid(self, form: RegisterForm) -> HttpResponse:
        messages.error(self.request, 'Wrong Information..')
        return super().form_invalid(form)


class Detail_View(DetailView):
    template_name = 'detail.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = context['object']
        context["favoiteForm"] = FavoriteForm(article.id)
        return context

class Favorite_View(LoginRequiredMixin, ListView, FormView):
    template_name = 'favorite.html' 
    model = UserFavoriteArticle
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    form_class = FavoriteForm

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form:FavoriteForm):
        article_id = form.cleaned_data['article']
        try:
            article=Article.objects.get(id=article_id)
        except Article.DoesNotExist as e:
            messages.error(
                    self.request, "Unsuccessful Add to favourite. Article.DoesNotExist")
        try:
            UserFavoriteArticle.objects.get(
                user=self.request.user,
                article=article,
            ).delete()
            messages.success(
                self.request, "successful Remove to favourite.")
        except UserFavoriteArticle.DoesNotExist as e:
            UserFavoriteArticle.objects.create(
                user=self.request.user,
                article=article,
            )
            messages.success(
                self.request, "successful Add to favourite.")
        return redirect('favorite')

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful Add to favourite. Invalid information.")
        return redirect('home')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(None, **self.get_form_kwargs())




class Publish(LoginRequiredMixin, FormView):
    template_name = "publish.html"
    form_class = PublishForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('index')

    def form_valid(self, form: PublishForm):
        title = form.cleaned_data['title']
        synopsis = form.cleaned_data['synopsis']
        content = form.cleaned_data['content']
        try:
            Article.objects.create(
                title=title,
                author=self.request.user,
                synopsis=synopsis,
                content=content
            )
        except DatabaseError as e:
            messages.success(
                self.request, "Unsuccessful publish. DatabaseError")
            return redirect('publish')
        messages.success(self.request, "Successful publish.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful publish. Invalid information.")
        return super().form_invalid(form)



def populate(request):
    movie_list = [
        {
            "title": "The Phantom Menace5",
            "author": "The Phantom Menace5",
            "synopsis": "Rick McCallum5",
            "content": "1999-05-195"
        },
        {
            "title": "The Phantom Menace6",
            "author": "The Phantom Menace6",
            "synopsis": "Rick McCallum6",
            "content": "1999-05-196"
        },
        {
            "title": "The Phantom Menace7",
            "author": "The Phantom Menace7",
            "synopsis": "Rick McCallum7",
            "content": "1999-05-197"
        },
        {
            "title": "The Phantom Menace8",
            "author": "The Phantom Menace8",
            "synopsis": "Rick McCallum8",
            "content": "1999-05-198"
        }
    ]
    result = []
    for i in movie_list:
        try:
            Article.objects.create(
                title=i['title'],
                synopsis=i['synopsis'],
                content=i['content'],
                author=request.user
            )
            result.append("OK")
        except Exception as e:
            print(e)
            result.append(e)
    return redirect(reverse_lazy('home'))
