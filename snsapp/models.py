from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField("auth.User", related_name="related_post", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return self.user.username
