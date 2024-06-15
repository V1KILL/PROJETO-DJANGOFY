from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, Perfil, render_module, render_video, CreateCheckoutSessionView, CancelView, SuccessView
urlpatterns = [
    path('', Home, name='home'),
    path('perfil', Perfil, name='perfil'),
    path('module/', render_module, name='module'),
    path('video/', render_video, name='video'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)