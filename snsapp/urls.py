from django.urls import path

from .views import (
    CreatePost,
    DeletePost,
    DetailPost,
    FollowDetail,
    FollowHome,
    FollowList,
    Home,
    LikeDetail,
    LikeHome,
    MyPost,
    UpdatePost,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("mypost", MyPost.as_view(), name="mypost"),
    path("home", Home.as_view(), name="home"),
    path("detail/<int:pk>", DetailPost.as_view(), name="detail"),
    path("detail/<int:pk>/update", UpdatePost.as_view(), name="update"),
    path("detail/<int:pk>/delete", DeletePost.as_view(), name="delete"),
    path("create/", CreatePost.as_view(), name="create"),
    # 一覧ページからいいねした場合と詳細ページからいいねした場合で分ける
    # TODO:いいねした時にリダイレクトさせずに同じページにとどまるようにJavascriptの非同期処理を実装する
    path("like-home/<int:pk>", LikeHome.as_view(), name="like-home"),
    path("like-detail/<int:pk>", LikeDetail.as_view(), name="like-detail"),
    path("follow-home/<int:pk>", FollowHome.as_view(), name="follow-home"),
    path("follow-detail/<int:pk>", FollowDetail.as_view(), name="follow-detail"),
    path("follow-list/", FollowList.as_view(), name="follow-list"),
]
