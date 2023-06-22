from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

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
