from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ViewHome, ViewPerfil, ViewRenderModule, ViewRenderVideo, CreateCheckoutSessionView, CancelView, SuccessView, ViewSignin, ViewSignup, ViewLogout, ViewLike, ViewCheck, ViewComment, ViewReply, ViewNewVideo, ViewNewTopicAndModule, ViewVideoEditPage, Edit, StripeIntentView, stripe_webhook,  ViewMudarNome, ViewMudarSenha, ViewMudarPerfil, ViewDeleteVideo, ViewDeleteModule, ViewDeleteTopic, ViewNewTopic, ViewPageEditModule, ViewEditModule
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
    path('new-topic/', ViewNewTopic, name='new-topic'),
    path('video-edit-page/', ViewVideoEditPage, name='video-edit-page'),
    

    path('page-edit-module/', ViewPageEditModule, name='page-edit-module'),
    
    path('edit-module/', ViewEditModule, name='edit-module'),

    path('edit/', Edit, name='edit'),

    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView, name='cancel'),

    path('success/', SuccessView, name='success'),

    path('mudar-nome/', ViewMudarNome, name='mudar-nome'),

    path('mudar-senha/', ViewMudarSenha, name='mudar-senha'),
    path('mudar-imagem/', ViewMudarPerfil, name='mudar-imagem'),
    path('delete-video/', ViewDeleteVideo, name='delete-video'),
    path('delete-module/', ViewDeleteModule, name='delete-module'),

    path('delete-topic/<int:topicId>', ViewDeleteTopic, name='delete-topic')
   
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)