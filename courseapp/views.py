from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout, update_session_auth_hash
from courseapp.models import Topic, Module, Comment, Video, UserProfile, User, Like, Check
from django.views.generic import TemplateView, View
import stripe
import json
from typing import Any

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='signin')
def ViewHome(request):
    topics = Topic.objects.all()
    modules = Module.objects.all()
    user = UserProfile.objects.get(user=request.user)
    context = {
        'topics':topics,
        'modules':modules,
        'user':user,
        'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'home/home.html', context)

def ViewSignin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            auth.login(request, user)
            return redirect('home')
        elif user is not None and not user.check_password(password):
            messages.info(request, 'Senha Incorreta')
            return redirect('signin')
        else:
            messages.info(request, 'Usuário Não Existe')
            return redirect('signin')
    return render(request, 'account/signin.html')

def ViewSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if username.isspace():
                messages.info(request, 'Nome Vazio')
                return redirect('signup')
            else:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Nome Existente')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    UserProfile.objects.create(user=user)
                    messages.info(request, 'Conta Criada com Sucesso')
                    return redirect('signin')
        else:
            messages.info(request, 'Senhas não coincidem')
            return redirect('register')
    else:
        return render(request, 'account/signup.html')

@login_required(login_url='signin')
def ViewLogout(request):
    logout(request)
    return render(request, 'account/signin.html')

@login_required
def ViewPerfil(request):
    user = UserProfile.objects.get(user_id=request.user.id)
    return render(request, 'visit-profile.html', {'user':user})

@login_required
def ViewRenderModule(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        module = Module.objects.get(id=data.get('moduleId'))
        mainvideo = module.videos.first()
        like = Like.objects.filter(user=request.user, video=mainvideo).exists()
        check = Check.objects.filter(user=request.user, video=mainvideo)
        comments = Comment.objects.filter(video=mainvideo)
        videos = Video.objects.filter(module=module).select_related('module')
        likes = Like.objects.filter(video=mainvideo)
        user_profile = UserProfile.objects.get(user=request.user)

        context = {
            'mainvideo':mainvideo, 
            'like':like,
            'check':check,
            'comments':comments,
            'videos':videos,
            'likes':likes,
            'module': module,
            'user':user_profile,
        }
        return render(request, 'module/video-page.html', context)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
@login_required
def ViewRenderVideo(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        topic = Topic.objects.get(id=data.get('topicId'))
        module = Module.objects.get(topic=topic, id=data.get('moduleId'))
        mainvideo = Video.objects.get(id=data.get('videoId'), module=module)

        comments = Comment.objects.filter(video=mainvideo)
        videos = Video.objects.filter(module=module)
        likes = Like.objects.filter(video=mainvideo)
        like = Like.objects.filter(user=request.user, video=mainvideo)
        check = Check.objects.filter(user=request.user, 
        video=mainvideo)
        user_profile = UserProfile.objects.get(user=request.user)
        
        context = {
            'mainvideo': mainvideo,
            'like':like,
            'check':check,
            'comments': comments,
            'videos': videos,
            'likes':likes,
            'module':module,
            'user':user_profile,
        }

        return render(request, 'module/video-page.html', context)
    
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def ViewLike(request):
    data = json.loads(request.body.decode('utf-8'))

    topic = Topic.objects.get(id=data.get('topicId'))
    module = Module.objects.get(topic=topic, id=data.get('moduleId'))
    mainvideo = Video.objects.get(module=module, id=data.get('videoId'))

    like = Like.objects.filter(user=request.user, video=mainvideo)
    check = Check.objects.filter(user=request.user, video=mainvideo)
    comments = Comment.objects.filter(video=mainvideo)
    videos = Video.objects.filter(module=module)
    likes = Like.objects.filter(video=mainvideo)
    user_profile = UserProfile.objects.get(user=request.user)

    if like:
        like.delete()
    else:
        like = Like.objects.create(user=request.user, video=mainvideo)
        like.save()

    context = {
        'mainvideo': mainvideo,
        'like':like,
        'check':check,
        'comments': comments,
        'videos':videos,
        'likes':likes,
        'module':module,
        'user':user_profile,
    }

    return render(request, 'module/video-page.html', context)

@login_required
def ViewCheck(request):
    data = json.loads(request.body.decode('utf-8'))

    topic = Topic.objects.get(id=data.get('topicId'))
    module = Module.objects.get(topic=topic, id=data.get('moduleId'))
    mainvideo = Video.objects.get(module=module, id=data.get('videoId'))

    like = Like.objects.filter(user=request.user, video=mainvideo)
    check = Check.objects.filter(user=request.user, video=mainvideo)
    comments = Comment.objects.filter(video=mainvideo)
    likes = Like.objects.filter(video=mainvideo)
    videos = Video.objects.filter(module=module)
    user = UserProfile.objects.get(user=request.user)

    if check:
        check.delete()
    else:
        check = Check.objects.create(user=request.user, video=mainvideo)
        check.save()

    context = {
        'mainvideo': mainvideo,
        'like':like,
        'check':check,
        'comments': comments,
        'module':module,
        'videos':videos,
        'likes':likes,
        'user':user,
    }

    return render(request, 'module/video-page.html', context)

def SuccessView(request):
    user = UserProfile.objects.get(user=request.user)
    user.status = True
    user.save()

    return render(request, 'success.html')

class CancelView(TemplateView):
    template_name = 'cancel.html'

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1:8000'
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'brl',
                            'unit_amount': 1000,
                            'product_data': {
                                'name': 'Curso',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'user_id': str(request.user.id)
                },
                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            customer = stripe.Customer.create(
                metadata={
                    'user_id': str(request.user.id)
                }
            )

            intent = stripe.PaymentIntent.create(
                amount=1000,
                currency='brl',
                customer=customer.id,
                metadata={
                    'user_id': str(request.user.id)
                }
            )
            return JsonResponse({'clientSecret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

import logging
logger = logging.getLogger(__name__)
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    logger.info(f"Webhook received: {event}")

    if event["type"] == "checkout.session.completed":
        intent = event['data']['object']
        user_id = intent['metadata']['user_id']
        print(user_id)
        logger.info(f"User ID from metadata: {user_id}")
        if user_id:
            try:
                user = UserProfile.objects.get(id=int(user_id))
                user.status = True
                user.save()
            except UserProfile.DoesNotExist:
                logger.error(f"User with ID {user_id} does not exist")
                pass  # Handle user not existing

    return JsonResponse({'status': 'success'}, status=200)

@csrf_exempt
@login_required
def ViewComment(request):
    data = json.loads(request.body.decode('utf-8'))

    topic = Topic.objects.get(id=data.get('topicId'))
    module = Module.objects.get(topic=topic, id= data.get('moduleId'))
    mainvideo = Video.objects.get(module=module, id=data.get('videoId'))

    like = Like.objects.filter(user=request.user, video=mainvideo)
    check = Check.objects.filter(user=request.user, video=mainvideo)
    videos = Video.objects.filter(module=module)
    comments = Comment.objects.filter(video=mainvideo)
    likes = Like.objects.all().filter(video=mainvideo)
    user_profile = UserProfile.objects.get(user=request.user)
    
    comentario = Comment.objects.create(user= user_profile, text=data.get('comentario'), video=mainvideo)
    comentario.save()

    context = {
        'mainvideo': mainvideo,
        'like':like,
        'check':check,
        'module':module,
        'likes':likes,
        'videos':videos,
        'comments': comments,
        'user':user_profile,
    }
    return render(request, 'module/video-page.html', context)

@login_required
def ViewReply(request):
    data = json.loads(request.body.decode('utf-8'))

    topic = Topic.objects.get(id=data.get('topicId'))
    module = Module.objects.get(topic=topic, id=data.get('moduleId'))
    mainvideo = Video.objects.get(module=module, id=data.get('videoId'))
    user_profile = UserProfile.objects.get(user=request.user)

    comentario = Comment.objects.get(video=mainvideo, id=data.get('comentarioId'))
    response = Comment.objects.create(video=mainvideo, text=data.get("comentario"), user=user_profile, response=comentario)
    response.save()
    
    like = Like.objects.filter(user=request.user, video=mainvideo)
    check = Check.objects.filter(user=request.user, video=mainvideo)
    videos = Video.objects.filter(module=module)
    comments = Comment.objects.filter(video=mainvideo)
    likes = Like.objects.filter(video=mainvideo)

    context = {
        'mainvideo': mainvideo,
        'like':like,
        'check':check,
        'videos':videos,
        'comments': comments,
        'module':module,
        'likes':likes,
        'user':user_profile,
        }
    
    return render(request, 'module/video-page.html', context)

@login_required
def ViewNewVideo(request):
    topics = Topic.objects.all()
    modules = Module.objects.all()
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':

        topic = Topic.objects.get(title=request.POST['topicoption'])
        module = Module.objects.get(topic=topic, title= request.POST['moduleoption'])
        video = Video.objects.create(module=module, title=request.POST["videotitle"], description=request.POST['videodescription'], url=request.POST['videourl'],image=request.FILES.get('thumbnail'))
        video.save()
        return redirect('home')
    
    context = {
        'modules':modules,
        'topics':topics,
        'user':user_profile,
    }

    return render(request, 'new-video.html', context)

@login_required
def ViewNewTopicAndModule(request):
    if request.method == 'POST':
        
        topic = Topic.objects.create(title=request.POST["topictitle"])
        module = Module.objects.create(title=request.POST['moduletitle'], description= request.POST['moduledescription'], topic=topic, image=request.FILES.get('thumbnail'), status=request.POST['videoversion'])
        module.save()
        return redirect('home')
    
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'new-topic-and-module.html', {'user':user_profile})

@login_required
def ViewVideoEditPage(request):

    data = json.loads(request.body.decode('utf-8'))

    topic = Topic.objects.get(id=data.get('topicId'))
    
    module = Module.objects.get(topic=topic, id=data.get('moduleId'))

    mainvideo = Video.objects.get(module=module, id=data.get('videoId'))

    user_profile = UserProfile.objects.get(user=request.user)
        
    context = {
        'mainvideo':mainvideo,
        'user':user_profile,
        'module':module,
        
    }
    return render(request, 'video-edit-page.html', context)

def Edit(request):
    if request.method == 'POST':
        try:
            topic_id = request.POST['topicId']
            module_id = request.POST['moduleId']
            video_id = request.POST['videoId']
            
            topic = Topic.objects.get(id=topic_id)
            module = Module.objects.get(topic=topic, id=module_id)
            mainvideo = Video.objects.get(module=module, id=video_id)

            mainvideo.title = request.POST['title']
            mainvideo.description = request.POST['description']
            mainvideo.url = request.POST['url']

            if request.FILES.get('capa'):
                mainvideo.image = request.FILES.get('capa')

            mainvideo.save()
            messages.success(request, 'Video Alterado Com Sucesso')
            return redirect('/')
        except KeyError as e:
            return render(request, 'error.html', {'message': f'KeyError: {e}'})

@login_required(login_url='login')
def ViewMudarNome(request):
    if User.objects.filter(username=request.POST['name']).exists():
        messages.error(request, 'Nome Existente')
        return redirect('perfil')
    else:
        request.user.username = request.POST['name']
        request.user.save()
    messages.success(request, 'Nome Alterado Com Sucesso')
    return redirect('perfil')

@login_required(login_url='login')
def ViewMudarSenha(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        request.user.set_password(password)
        request.user.save()
        update_session_auth_hash(request, request.user)
    messages.success(request, 'Senha Alterada')
    return redirect('perfil')

@login_required(login_url='login')
def ViewMudarPerfil(request):
    if request.method == 'POST':
        image = request.FILES['image']
        user = UserProfile.objects.get(user=request.user)
        user.profileimg = image
        user.save()
    messages.success(request, 'Imagem alterada')
    return redirect('perfil')           

def ViewDeleteVideo(request):
    data = json.loads(request.body.decode('utf-8'))

    topic = Topic.objects.get(id=data.get('topicId'))
    module = Module.objects.get(id=data.get('moduleId'), topic=topic)
    video = Video.objects.get(id=data.get('videoId'), module=module)

    video.delete()
    

    messages.success(request, 'Vídeo Removido Com Sucesso') 
    return redirect("/")

def ViewDeleteModule(request):
    data = json.loads(request.body.decode('utf-8'))

    topic = Topic.objects.get(id=data.get('topicId'))
    module = Module.objects.get(id=data.get('moduleId'), topic=topic)
    

    module.delete()
    

    messages.success(request, 'Módulo Removido Com Sucesso') 
    return redirect("/")

def ViewDeleteTopic(request, topicId):
    topic = Topic.objects.get(id=topicId)
    topic.delete()

    messages.success(request, 'Tópico Removido Com Sucesso')
    return redirect('/')