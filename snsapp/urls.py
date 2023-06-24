from django.urls import path

from .views import CreatePost, DetailPost, Home, MyPost, UpdatePost

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("mypost", MyPost.as_view(), name="mypost"),
    path("home", Home.as_view(), name="home"),
    path("detail/<int:pk>", DetailPost.as_view(), name="detail"),
    path("detail/<int:pk>/update", UpdatePost.as_view(), name="update"),
    path("create/", CreatePost.as_view(), name="create"),
]
