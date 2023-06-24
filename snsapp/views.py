from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

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
