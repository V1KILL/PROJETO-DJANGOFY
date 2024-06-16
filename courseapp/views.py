from django.shortcuts import render, redirect
from courseapp.models import Topic, Module, Comment, Video
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import stripe
from typing import Any
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView, View


def Home(request):
    topics = Topic.objects.all()
    modules = Module.objects.all()
    content = {
        'topics':topics,
        'modules':modules,
        
    }
    return render(request, 'index.html', content)

def Perfil(request):
    return render(request, 'perfil.html')

@csrf_exempt
def render_module(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        module_id = data.get('moduleId')
        print('Module ID recebido:', module_id)

        module = Module.objects.get(id=module_id)
        mainvideo = module.videos.first()
        comments = Comment.objects.filter(video=mainvideo)
        videos = Video.objects.filter(module = module)
        return render(request, 'videopage.html', {'module': module, 'mainvideo':mainvideo, 'comments':comments, 'videos':videos})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def render_video(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        video_id = data.get('videoId')
        print('Video ID recebido:', video_id)
    
        video = Video.objects.get(id=video_id)
        module = video.module
        comments = Comment.objects.filter(video=video)
        videos = Video.objects.filter(module=module)
        context = {
            'mainvideo': video,
            'comments': comments,
            'videos': videos
        }
        return render(request, 'videopage.html', context)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

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