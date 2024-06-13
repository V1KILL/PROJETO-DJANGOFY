from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, Perfil, render_module
urlpatterns = [
    path('', Home, name='home'),
    path('perfil', Perfil, name='perfil'),
    path('module/', render_module, name='module'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)