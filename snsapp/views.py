from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Post


# Create your views here.
# LoginRequiredMixin: ログインしていなければ一覧ページを参照することができない
class Home(LoginRequiredMixin, ListView):
    model = Post
    template_name = "list.html"

    # 自分以外の投稿に限定
    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user)


class MyPost(LoginRequiredMixin, ListView):
    model = Post
    template_name = "list.html"

    # 自分の投稿に限定
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class DetailPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "detail.html"


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "create.html"
    fields = ["title", "body"]
    success_url = reverse_lazy("mypost")

    def form_valid(self, form):
        # 投稿ユーザーをリクエストユーザーと紐付ける処理
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "update.html"
    fields = ["title", "body"]
    success_url = reverse_lazy("mypost")

    def get_success_url(self, **kwargs):
        # 編集完了後の遷移先
        pk = self.kwargs["pk"]
        return reverse_lazy("detail", kwargs={"pk": pk})

    def test_func(self, **kwargs):
        # アクセスできるユーザーを制限
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return post.user == self.request.user


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("mypost")

    def test_func(self, **kwargs):
        # アクセスできるユーザーを制限
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return post.user == self.request.user


class LikeBase(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kargs["pk"]
        related_post = Post.objects.get(pk=pk)

        # いいねテーブル内にすでにユーザーが存在する場合
        if self.request.user in related_post.like.all():
            obj = related_post.like.remove(self.request.user)
        else:
            # テーブルにユーザーを追加
            obj = related_post.like.add(self.request.user)
        return obj


class LikeHome(LikeBase):
    def get(self, request, *args, **kwargs):
        # LikeBaseでリターンしたobj情報を継承
        # super().get(request, *args, **kwargs)
        LikeBase().get(request, *args, **kwargs)
        # homeにリダイレクト
        return redirect("home")


class LikeDetail(LikeBase):
    def get(self, request, *args, **kwargs):
        # LikeBaseでリターンしたobj情報を継承
        # super().get(request, *args, **kwargs)
        LikeBase().get(request, *args, **kwargs)
        pk = self.kwargs["pk"]
        # detailにリダイレクト
        return redirect("detail", pk)
