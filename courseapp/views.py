from django.shortcuts import render, redirect
from .models import Topic, Module

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
