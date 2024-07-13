from django.contrib import admin
from .models import Video, Module, Topic, Comment, UserProfile, Like, Check
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Check)
admin.site.register(Module)
admin.site.register(Topic)
admin.site.register(Comment)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'status')  # Adicione 'id' na lista de campos a serem exibidos
    # Aqui, 'name', 'email', 'status' são outros campos do seu modelo UserProfile.
    # Substitua-os pelos campos relevantes para o seu modelo.

    # Se quiser adicionar filtros e pesquisas, pode fazer assim:
    list_filter = ('status',)
   

admin.site.register(UserProfile, UserProfileAdmin)
