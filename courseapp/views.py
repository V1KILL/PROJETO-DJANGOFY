from django.shortcuts import render, redirect
from courseapp.models import Topic, Module

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

def render_module(request):
    if request.method == 'POST':
        id = request.POST.get('moduleId')
        
        module = Module.objects.get(id=id)
        return render(request, 'videopage.html',{'module':module})
    return render(request, 'index.html')
