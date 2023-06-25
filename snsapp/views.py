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

from .models import Connection, Post


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


class FollowBase(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ユーザーの特定
        pk = self.kwargs["pk"]
        target_user = Post.objects.get(pk=pk).user

        # ユーザー情報よりコネクション情報を取得。存在しなければ作成
        my_connection = Connection.objects.get_or_create(user=self.request.user)
        # フォローテーブル内にすでにユーザーが存在する場合
        if target_user in my_connection[0].following.all():
            # テーブルからユーザーを削除
            obj = my_connection[0].following.remove(target_user)
        # フォローテーブル内にすでにユーザーが存在しない場合
        else:
            # テーブルにユーザーを追加
            obj = my_connection[0].following.add(target_user)
        return obj


class FollowHome(FollowBase):
    """HOMEページでフォローした場合"""

    def get(self, request, *args, **kwargs):
        # FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        # homeにリダイレクト
        return redirect("home")


class FollowDetail(FollowBase):
    """詳細ページでフォローした場合"""

    def get(self, request, *args, **kwargs):
        # FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs["pk"]
        # detailにリダイレクト
        return redirect("detail", pk)


class FollowList(LoginRequiredMixin, ListView):
    """フォローしたユーザーの投稿をリスト表示"""

    model = Post
    template_name = "list.html"

    def get_queryset(self):
        """フォローリスト内にユーザーが含まれている場合のみクエリセット返す"""
        my_connection = Connection.objects.get_or_create(user=self.request.user)
        all_follow = my_connection[0].following.all()
        # 投稿ユーザーがフォローしているユーザーに含まれている場合オブジェクトを返す。
        return Post.objects.filter(user__in=all_follow)

    def get_context_data(self, *args, **kwargs):
        """コネクションに関するオブジェクト情報をコンテクストに追加"""
        context = super().get_context_data(*args, **kwargs)
        # コンテクストに追加
        context["connection"] = Connection.objects.get_or_create(user=self.request.user)
        return context
