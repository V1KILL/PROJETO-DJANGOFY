from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ViewHome, ViewPerfil, ViewRenderModule, ViewRenderVideo, CreateCheckoutSessionView, CancelView, SuccessView, ViewSignin, ViewSignup, ViewLogout, ViewLike, ViewCheck, ViewComment, ViewReply, ViewNewVideo, ViewNewTopicAndModule, ViewVideoEditPage, Edit

urlpatterns = [
    path('', ViewHome, name='home'),

    path('perfil/', ViewPerfil, name='perfil'),

    path('module/', ViewRenderModule, name='module'),

    path('video/', ViewRenderVideo, name='video'),

    path('signin/', ViewSignin, name='signin'),

    path('signup/', ViewSignup, name='signup'),

    path('logout/', ViewLogout, name='logout'),

    path('like/', ViewLike, name='like'),

    path('check/', ViewCheck, name='check'),

    path('comment/', ViewComment, name='comment'),
    
    path('reply/', ViewReply, name='reply'),

    path('new-video/', ViewNewVideo, name='new-video'),

    path('new-topic-and-module/', ViewNewTopicAndModule, name='new-topic-and-module'),
    path('video-edit-page/', ViewVideoEditPage, name='video-edit-page'),
    path('edit/', Edit, name='edit'),

    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),

    path('cancel/', CancelView.as_view(), name='cancel'),

    path('success/', SuccessView.as_view(), name='success'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)