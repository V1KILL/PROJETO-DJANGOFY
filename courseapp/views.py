from django.shortcuts import render, redirect
from django.http import JsonResponse
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

@login_required(login_url='login')
def Home(request):
    topics = Topic.objects.all()
    modules = Module.objects.all()
    user = UserProfile.objects.get(user=request.user)
    context = {
        'topics':topics,
        'modules':modules,
        'user':user,
    }
    return render(request, 'index.html', context)

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

@login_required
def Perfil(request):
    user = UserProfile.objects.get(user_id=request.user.id)
    return render(request, 'perfil.html', {'user':user})

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
        return render(request, 'videopage.html', context)
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

        return render(request, 'videopage.html', context)
    
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

    return render(request, 'videopage.html', context)

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
@login_required
def ViewComentar(request):
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
    return render(request, 'videopage.html', context)

@login_required
def ViewResponder(request):
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
    
    return render(request, 'videopage.html', context)

@login_required
def ViewCreateVideo(request):
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

    return render(request, 'postar2.html', context)

@login_required
def ViewCreateTopicAndModule(request):
    if request.method == 'POST':
        
        topic = Topic.objects.create(title=request.POST["topictitle"])
        module = Module.objects.create(title=request.POST['moduletitle'], description= request.POST['moduledescription'], topic=topic, image=request.FILES.get('thumbnail'), status=request.POST['videoversion'])
        module.save()
        return redirect('home')
    
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'postar.html', {'user':user_profile})