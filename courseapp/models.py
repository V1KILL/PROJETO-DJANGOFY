from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(upload_to='profiles/', default='profiles/blankperfil.jpg')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

class Topic(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='module/',default='module/code bg.webp')
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    classes = models.IntegerField(default=0)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.title
    
    def formatted_date(self):
        return self.date.strftime("%d, %B, %Y")

class Video(models.Model):
    url = models.TextField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='videos')
    image = models.ImageField(upload_to='video/',default='video/code bg.webp')

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    response = models.ForeignKey('self', on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    text = models.TextField()
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    

    def __str__(self):
        return f'Comentário de {self.user.user.username}'