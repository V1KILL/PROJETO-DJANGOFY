from django.shortcuts import render, redirect
from courseapp.models import Topic, Module, Comment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

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
        print('Module ID recebido:', module_id)  # Verifica no console do servidor Django

        module = Module.objects.get(id=module_id)
        mainvideo = module.videos.first()
        comments = Comment.objects.filter(video=mainvideo)
        return render(request, 'videopage.html', {'module': module, 'mainvideo':mainvideo, 'comments':comments})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
