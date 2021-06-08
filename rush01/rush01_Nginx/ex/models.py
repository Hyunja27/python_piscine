from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import Expression
from django.db.models.query_utils import select_related_descend
from django.db.utils import DatabaseError


class UpVoteModel(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class DownVoteModel(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class TipModel(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now_add=True)
    up_votes = models.ManyToManyField(UpVoteModel)
    down_votes = models.ManyToManyField(DownVoteModel)
    updated_at = models.DateTimeField(auto_now=True)

    def upvote(self, user):
        try:
            down_vote: DownVoteModel = self.down_votes.get(author=user)
            down_vote.delete()
        except DownVoteModel.DoesNotExist as e:
            pass
        try:
            up_vote: UpVoteModel = self.up_votes.get(author=user)
            up_vote.delete()
        except UpVoteModel.DoesNotExist as e:
            up_vote = UpVoteModel(author=user)
            up_vote.save()
            self.up_votes.add(up_vote)
            self.save()

    def downvote(self, user):
        try:
            up_votes: UpVoteModel = self.up_votes.get(author=user)
            up_votes.delete()
        except UpVoteModel.DoesNotExist as e:
            pass
        try:
            down_vote: DownVoteModel = self.down_votes.get(author=user)
            down_vote.delete()
        except DownVoteModel.DoesNotExist as e:
            down_vote = DownVoteModel(author=user)
            down_vote.save()
            self.down_votes.add(down_vote)
            self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # User모델과 Profile을 1:1로 연결
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField(blank=True)
    # email =
    # first_name =
    # last_name =


class Article(models.Model):
    title = models.CharField(max_length=64, null=False)
    author = models.ForeignKey(
        User, related_name="article", on_delete=models.CASCADE, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    # synopsis = models.CharField(max_length=312, null=False)
    content = models.TextField(null=False)

    # 내림차순
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.CharField("reply", max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, related_name="Comment", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.body


class ReComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    body = models.CharField("Re_reply", max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, related_name="Recomment", on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return self.body
