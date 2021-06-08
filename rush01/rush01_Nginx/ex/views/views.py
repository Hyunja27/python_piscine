from typing import Any, Dict
from django.db.utils import DatabaseError
from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, DetailView, ListView
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import db
from django.shortcuts import render, get_object_or_404
from rush01 import settings
from django.conf.urls.static import static


from ex.forms.forms import (
    TipForm,
    DeleteTipForm,
    VoteForm,
    CustomUserChangeForm,
    ProfileForm,
    RegisterForm,
    PublishForm,
    CommentForm,
    ReCommentForm,
)
from ex.models import TipModel, Profile, Article, ReComment
from django.urls import reverse_lazy


class Index(View):
    template_name = "index.html"

    def get(self, request):
        try:
            tips = TipModel.objects.all().order_by("-date")

        except db.DatabaseError as e:
            tips = []
        context = {
            "tipform": TipForm(),
            "tips": [
                {
                    "id": tip.id,
                    "content": tip.content,
                    "author": tip.author,
                    "date": tip.date,
                    "up_votes": tip.up_votes,
                    "down_votes": tip.down_votes,
                    "deleteform": DeleteTipForm(tip.id),
                    "voteform": VoteForm(tip.id),
                }
                for tip in tips
            ],
        }
        print([(tip.up_votes.count(), tip.down_votes.count()) for tip in tips])
        return render(request, self.template_name, context)


class Logout(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("login")


class Show_Page(View):
    template_name = "mainpage.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class Register(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("publication")

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, "You already logined!")
            return redirect("publication")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: RegisterForm):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Unsuccessful registration. Invalid information.")
        return super().form_invalid(form)


class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("publication")

    # def get_initial(self) -> Dict[str, Any]:
    #     initial = super().get_initial()
    #     initial['username'] = self.request.username
    #     initial['first_name'] = self.request.first_name
    #     initial['last_name'] = self.request.last_name
    #     initial['email'] = self.request.id
    #     initial['content'] = self.request.content
    #     initial['author'] = self.request.author
    #     initial['image'] = self.request.image
    #     initial['nickname'] = self.request.nickname
    #     initial['description'] = self.request.description
    #     return initial

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, "You already logined!")
            return redirect("publication")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: AuthenticationForm):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
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
    http_method_names = ["post", "put", "delete"]
    login_url = reverse_lazy("login")

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get("_method", "").lower()
        if method == "put":
            return self.put(*args, **kwargs)
        if method == "delete":
            return self.delete(*args, **kwargs)
        return super(Tip, self).dispatch(*args, **kwargs)

    def post(self, request):
        form = TipForm(request.POST)
        if form.is_valid():
            try:
                TipModel.objects.create(
                    content=form.cleaned_data["content"], author=self.request.user
                )
                messages.success(self.request, "Successful create Tip.")
            except DatabaseError as e:
                print(e)
                messages.error(self.request, "Unsuccessful create Tip. (db error)")
        else:
            messages.error(
                self.request, "Unsuccessful create Tip. (Invalid form data.)"
            )
        return redirect("publication")

    def __error_msg(self, method, msg):
        messages.error(self.request, f"Unsuccessful {method} Tip. ({msg})")
        return redirect("publication")

    def delete(self, request: HttpRequest):
        form = DeleteTipForm(None, request.POST)
        if not form.is_valid():
            return self.__error_msg("delete", "Invaild form data.")
        try:
            tip: TipModel = TipModel.objects.get(id=form.cleaned_data["id"])
            if (
                tip.author != request.user
                and request.user.is_staff == False
                and request.user.is_superuser == False
            ):
                return self.__error_msg("delete", "access denied")
            tip.delete()
            messages.success(self.request, "Successful Erase Tip.")
        except TipModel.DoesNotExist as e:
            return self.__error_msg("delete", "Tip does not exist")
        except DatabaseError as e:
            return self.__error_msg("delete", "db error")

        return redirect("publication")

    def put(self, request):
        form = VoteForm(None, request.POST)
        if not form.is_valid():
            return self.__error_msg("vote", "Invaild form data.")
        try:
            tip: TipModel = TipModel.objects.get(id=form.cleaned_data["id"])
            if form.cleaned_data["type"]:
                tip.upvote(request.user)
            elif (
                tip.author != request.user
                and request.user.groups.filter(name="NoNo").exists()
            ):
                return self.__error_msg("vote", "Oh... You are a NoNo User! No!!")
            else:
                tip.downvote(request.user)
        except TipModel.DoesNotExist as e:
            return self.__error_msg("vote", "Tip does not exist")
        except DatabaseError as e:
            return self.__error_msg("vote", "db error")
        messages.success(request, "Dood Voted!")
        return redirect("publication")


def Profile_Edit(request):
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            "12345",
            "6789",
            "image_hahehihoho",
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect("publication")
        return redirect("profile")
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm(
            "12345", "6789", "image_hahehihoho", instance=profile
        )
        return render(
            request,
            "profile.html",
            {"user_change_form": user_change_form, "profile_form": profile_form},
        )


class ArticleView(ListView):
    paginate_by = 10
    template_name = "post.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


# class Detail_View(DetailView):
#     template_name = "post_detail.html"
#     model = Article

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(context)
#         return context


def article_detail(request, pk):

    article = get_object_or_404(Article, pk=pk)

    # 만약 post일때만 댓글 입력에 관한 처리를 더한다.
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        comment_form.instance.author_id = request.user.id
        comment_form.instance.document_id = pk
        if comment_form.is_valid():
            comment = comment_form.save()

    # models.py에서 document의 related_name을 comments로 해놓았다.

    comment_form = CommentForm()
    comments = Article.objects.get(id=pk)
    recomment_form = ReCommentForm()

    return render(
        request,
        "post_detail.html",
        {
            "object": article,
            "comments": comments,
            "comment_form": comment_form,
            "recomment_form": recomment_form,
        },
    )


class Create_comment(View):
    def get(self, request, commnets_id):
        return redirect(
            "detail", commnets_id
        )  # redirect('애칭', parameter) 해주면 google.com/1 이런식으로 뒤에 붙는 값을 지정해줄수있다.

    def post(self, request, commnets_id):
        filled_form = CommentForm(request.POST)
        if filled_form.is_valid():
            temp_form = filled_form.save(commit=False)
            temp_form.post = Article.objects.get(id=commnets_id)
            temp_form.author = self.request.user
            temp_form.save()
        return redirect(
            "detail", commnets_id
        )  # redirect('애칭', parameter) 해주면 google.com/1 이런식으로 뒤에 붙는 값을 지정해줄수있다.

def Create_recomment(request, commnets_id):
    filled_form = ReCommentForm(request.POST) 

    if filled_form.is_valid():
        recomment = filled_form.save(commit=False)
        print(recomment.comment, recomment.body)
        recomment.author = request.user
        recomment.save()
    return redirect('detail', commnets_id)


class Publish(LoginRequiredMixin, FormView):
    template_name = "publish.html"
    form_class = PublishForm
    success_url = reverse_lazy("publication")
    login_url = reverse_lazy("login")

    def form_valid(self, form: PublishForm):
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        try:
            Article.objects.create(
                title=title, author=self.request.user, content=content
            )
        except DatabaseError as e:
            messages.success(self.request, "Unsuccessful publish. DatabaseError")
            return redirect("publish")
        messages.success(self.request, "Successful publish.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Unsuccessful publish. Invalid information.")
        return super().form_invalid(form)


class PublicView(ListView):
    paginate_by = 10
    template_name = "post.html"
    model = Article

    def get_queryset(self):
        return self.model.objects.all()


def Admin_edit(request):
    return redirect("admin")
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            "12345",
            "6789",
            "image_hahehihoho",
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect("index")
        return redirect("profile")
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm(
            "12345", "6789", "image_hahehihoho", instance=profile
        )
        return render(
            request,
            "profile.html",
            {"user_change_form": user_change_form, "profile_form": profile_form},
        )
