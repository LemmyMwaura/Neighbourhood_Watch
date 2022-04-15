from django.shortcuts import render, redirect
from base.models import Neighbourhood, Post, Profile, Business
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(user__username__icontains = q) |
        Q(hood__name__icontains = q) |
        Q(message__icontains = q)
    )
    neighbourhoods = Neighbourhood.objects.all()

    context = {"neighbourhoods":neighbourhoods}
    return render(request,'base/home.html',context)