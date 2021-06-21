from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import (
    ContentType,
)
from django.db import models


class UserProfile(models.Model):
    last_login = models.DateTimeField(null=True, blank=True)
    last_request = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    text = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    likes = GenericRelation('Like')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    @property
    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateField(auto_now_add=True)
