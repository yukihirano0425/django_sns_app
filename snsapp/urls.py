from django.urls import path

from .views import DetailPost, Home, MyPost

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("mypost", MyPost.as_view(), name="mypost"),
    path("home", Home.as_view(), name="home"),
    path("detail/<int:pk>", DetailPost.as_view(), name="detail"),
]
