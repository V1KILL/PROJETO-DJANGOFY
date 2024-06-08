from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Topic(models.Model):
    title = models.CharField(max_length=200)
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.title

class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='module/',default='1708190589974.jpg')
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    classes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Video(models.Model):
    url = models.TextField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='videos')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    response = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.user} on {self.date}'