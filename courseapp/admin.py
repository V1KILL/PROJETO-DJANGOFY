from django.contrib import admin
from .models import Video, Module, Topic, Comment, UserProfile, Like, Check
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Check)
admin.site.register(Module)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(UserProfile)


