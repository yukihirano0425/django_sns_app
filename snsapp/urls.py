from django.urls import path

from .views import Home, MyPost

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("mypost", MyPost.as_view(), name="mypost"),
]
