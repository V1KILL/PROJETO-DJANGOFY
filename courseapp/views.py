from django.shortcuts import render, redirect
from courseapp.models import Topic, Module, Comment, Video, UserProfile, User, Like, Check
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import stripe
from typing import Any
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash

@login_required(login_url='login')
def Home(request):
    topics = Topic.objects.all()
    modules = Module.objects.all()

    user = UserProfile.objects.get(user=request.user)
    print(user)
    content = {
        'topics':topics,
        'modules':modules,
        'user':user,
    }
    return render(request, 'index.html', content)

def ViewLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            auth.login(request, user)
            return redirect('home')
        elif user is not None and not user.check_password(password):
            messages.info(request, 'Senha Incorreta')
            return redirect('login')
        else:
            messages.info(request, 'Usuário Não Existe')
            return redirect('login')
    return render(request, 'login.html')


def ViewRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if username.isspace():
                messages.info(request, 'Nome Vazio')
                return redirect('register')
            else:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Nome Existente')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    UserProfile.objects.create(user=user)
                    messages.info(request, 'Conta Criada com Sucesso')
                    return redirect('login')
        else:
            messages.info(request, 'Senhas não coincidem')
            return redirect('register')
    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def ViewLogout(request):
    
    logout(request)
    return render(request, 'login.html')

def Perfil(request):
    user = User.objects.get(id=request.user.id)
    user = UserProfile.objects.get(user=user)
    return render(request, 'perfil.html', {'user':user})

@csrf_exempt
def render_module(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        module_id = data.get('moduleId')
        print('Module ID recebido:', module_id)

        module = Module.objects.get(id=module_id)
        mainvideo = module.videos.first()
        like = Like.objects.filter(user=request.user, video=mainvideo).exists()
        comments = Comment.objects.filter(video=mainvideo)
        videos = Video.objects.filter(module = module)
        likes = Like.objects.all().filter(video=mainvideo)
        check = Check.objects.filter(video=mainvideo, user=request.user)
        user = UserProfile.objects.get(user=request.user)
        return render(request, 'videopage.html', {'module': module, 'mainvideo':mainvideo, 'comments':comments, 'videos':videos, 'like':like, 'likes':likes, 'check':check, 'user':user})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_exempt
def render_video(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        video_id = data.get('videoId')
        topicId = data.get('topicId')
        moduleId = data.get('moduleId')
        print('Video ID recebido:', video_id)
        print(f'topic id{ topicId}')
        topic = Topic.objects.get(id=topicId)
        module = Module.objects.get(topic=topic, id=moduleId)
        video = Video.objects.get(id=video_id, module=module)
        comments = Comment.objects.filter(video=video)
        videos = Video.objects.filter(module=module)
        likes = Like.objects.all().filter(video=video)
        like = Like.objects.filter(user=request.user, video=video)
        check = Check.objects.filter(user=request.user, video=video)
        user = UserProfile.objects.get(user=request.user)
        
        context = {
            'mainvideo': video,
            'comments': comments,
            'videos': videos,
            'likes':likes,
            'module':module,
            'like':like,
            'check':check,
            'user':user,
        }
        return render(request, 'videopage.html', context)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

def ViewLike(request):
    print('tudo certo')
    data = json.loads(request.body.decode('utf-8'))
    moduleId = data.get('moduleId')
    videoId = data.get('videoId')
    topicId = data.get('topicId')

    topic = Topic.objects.get(id=topicId)
    module = Module.objects.get(topic=topic, id=moduleId)
    mainvideo = Video.objects.get(module=module, id=videoId)

    like = Like.objects.filter(user=request.user, video=mainvideo)
    likes = Like.objects.all().filter(video=mainvideo)
    videos = Video.objects.filter(module=module)
    comments = Comment.objects.filter(video=mainvideo)
    check = Check.objects.filter(user=request.user, video=mainvideo)
    user = UserProfile.objects.get(user=request.user)
    if like:
        like.delete()
    else:
        like = Like.objects.create(user=request.user, video=mainvideo)
        like.save()

    context = {
        'like':like,
        'likes':likes,
        'module':module,
        'mainvideo': mainvideo,
        'videos':videos,
        'comments': comments,
        'check':check,
        'user':user,
    }

    return render(request, 'videopage.html', context)

def ViewCheck(request):
    print('tudo certo')
    data = json.loads(request.body.decode('utf-8'))
    moduleId = data.get('moduleId')
    videoId = data.get('videoId')
    topicId = data.get('topicId')

    topic = Topic.objects.get(id=topicId)
    module = Module.objects.get(topic=topic, id=moduleId)
    mainvideo = Video.objects.get(module=module, id=videoId)

    check = Check.objects.filter(user=request.user, video=mainvideo)
    like = Like.objects.filter(user=request.user, video=mainvideo)
    videos = Video.objects.filter(module=module)
    comments = Comment.objects.filter(video=mainvideo)
    likes = Like.objects.all().filter(video=mainvideo)
    user = UserProfile.objects.get(user=request.user)
    if check:
        check.delete()
    else:
        check = Check.objects.create(user=request.user, video=mainvideo)
        check.save()

    context = {
        'check':check,
        'module':module,
        'like':like,
        'likes':likes,
        'mainvideo': mainvideo,
        'videos':videos,
        'comments': comments,
        'user':user,
    }

    return render(request, 'videopage.html', context)

class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelView(TemplateView):
    template_name = 'cancel.html'
    
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        
        
        YOUR_DOMAIN = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                   'price_data': {
                        'currency':'brl',
                        'unit_amount':1000,
                        'product_data': {
                            'name':'Curso Premium',
                        }
                   },
                    
                    'quantity': 1,
                },
            ],
            
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({
            'id':checkout_session.id
        }
        )

@csrf_exempt
def ViewComentar(request):
    print('cheguei')
    data = json.loads(request.body.decode('utf-8'))
    comentario = data.get("comentario")
    moduleId = data.get('moduleId')
    videoId = data.get('videoId')
    topicId = data.get('topicId')
    print(comentario)

    topic = Topic.objects.get(id=topicId)
    module = Module.objects.get(topic=topic, id=moduleId)
    mainvideo = Video.objects.get(module=module, id=videoId)
    user = UserProfile.objects.get(user=request.user)
    comentario = Comment.objects.create(user= user, text=comentario, video=mainvideo)
    comentario.save()
    check = Check.objects.filter(user=request.user, video=mainvideo)
    like = Like.objects.filter(user=request.user, video=mainvideo)
    videos = Video.objects.filter(module=module)
    comments = Comment.objects.filter(video=mainvideo)
    likes = Like.objects.all().filter(video=mainvideo)
    context = {
        'check':check,
        'module':module,
        'like':like,
        'likes':likes,
        'mainvideo': mainvideo,
        'videos':videos,
        'comments': comments,
        'user':user
    }
    return render(request, 'videopage.html', context)

def ViewResponder(request):
    print('cheguei')
    data = json.loads(request.body.decode('utf-8'))
    resposta = data.get("comentario")
    moduleId = data.get('moduleId')
    videoId = data.get('videoId')
    topicId = data.get('topicId')
    comentarioId = data.get('comentarioId')
   

    topic = Topic.objects.get(id=topicId)
    module = Module.objects.get(topic=topic, id=moduleId)
    mainvideo = Video.objects.get(module=module, id=videoId)
    user = UserProfile.objects.get(user=request.user)
    comentario = Comment.objects.get(video=mainvideo, id=comentarioId)
    response = Comment.objects.create(video=mainvideo, text=resposta, user=user, response=comentario)
    response.save()
    
    check = Check.objects.filter(user=request.user, video=mainvideo)
    like = Like.objects.filter(user=request.user, video=mainvideo)
    videos = Video.objects.filter(module=module)
    comments = Comment.objects.filter(video=mainvideo)
    likes = Like.objects.all().filter(video=mainvideo)
    context = {
        'check':check,
        'module':module,
        'like':like,
        'likes':likes,
        'mainvideo': mainvideo,
        'videos':videos,
        'comments': comments,
        'user':user,
        }
    return render(request, 'videopage.html', context)

def ViewCreateVideo(request):
    return render(request, 'postar2.html')

def ViewCreateTopicAndModule(request):
    return render(request, 'postar.html')