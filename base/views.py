from django.shortcuts import render, redirect
from base.forms import UserRegistrationForm
from base.models import Neighbourhood, Post, Profile, Business
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(user__user_profile__username__icontains = q) |
        Q(hood__name__icontains = q) |
        Q(message__icontains = q)
    )
    neighbourhoods = Neighbourhood.objects.all()

    context = {"neighbourhoods":neighbourhoods, "posts":posts}
    return render(request,'base/home.html',context)

def login_user(request):
    page='login'

    if request.user.is_authenticated:
        messages.success(request, 'Already logged in')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password) 

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {request.user.username}') 
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context={"page":page}
    return render(request, 'base/login_register.html', context)

def register_user(request):
    page = 'register'
    form = UserRegistrationForm

    try:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                messages.success(request, f'Hi {request.user.username}, Your account was successfully created')
                return redirect('home')
            else:
                messages.error(request, 'An error occured during registration, Try again')
    except Exception as e:
        messages.error(request, 'Something went wrong. Probably a connection issue, Try again!')

    context={"page":page, "form":form}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def profile(request,pk):

    context={}
    return render(request, 'base/profile', context)
