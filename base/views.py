from django.shortcuts import render, redirect
from base.forms import BusinessForm, PostForm, UserRegistrationForm, ProfileForm
from base.models import Neighbourhood, Post, Profile, Business
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def home(request):
    neighbourhoods = Neighbourhood.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(user__user_profile__username__icontains = q) |
        Q(hood__name__icontains = q) |
        Q(message__icontains = q)
    )
    form = PostForm

    context = {"neighbourhoods":neighbourhoods, "posts":posts, "form":form}
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
        messages.error(request, 'Something went wrong. Probably a connection issue, Try again!', e)

    context={"page":page, "form":form}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def create_post(request):
    current_user_profile = Profile.objects.get(id=request.user.id)

    if request.method == 'POST':
        try:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user_id = current_user_profile.id
                post.hood_id = current_user_profile.users_neighbourhood.id
                post.save()
                messages.success(request, 'Your post was created')
                return redirect('home')
            else:
                messages.error(request, 'Something went wrong')
        except Exception as e:
            messages.error(request, 'Error')

@login_required(login_url='login')
def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        try:
            post.delete()
            messages.success(request, 'Post was deleted')
            return redirect('home')
        except Exception:
            messages.error(request, 'Could not delete post, Try again')

    context = {"obj":post}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def update_post(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        try:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your post was edited')
                return redirect('home')
            else:
                messages.error(request, 'Something went wrong')
        except Exception as e:
            messages.error(request, 'Error')

    context = {"form":form}
    return render(request,'base/edit_post.html', context)

@login_required(login_url='login')
def neighbourhood(request,pk):
    neighbourhoods = Neighbourhood.objects.all()
    hood = Neighbourhood.objects.get(id=pk)
    posts = hood.posts.all()
    businesses = hood.business_set.all()
    members = hood.members.all()
    form = BusinessForm

    context = {"hood":hood, "posts":posts, "members":members,
        "form":form, "neighbourhoods":neighbourhoods, "businesses":businesses }
    return render(request, 'base/hood.html', context)

@login_required(login_url='login')
def create_business(request,pk):
    current_user_profile = Profile.objects.get(id=request.user.id)

    if request.method == 'POST':
        try:
            form = BusinessForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.users_name_id = current_user_profile.id
                post.Neighbourhood_bsns_id = pk
                post.save()
                messages.success(request, 'Your Business was posted')
                return redirect('open-hood', pk=pk)
            else:
                messages.error(request, 'Something went wrong, Your business wasn\'t posted, Try again.')
        except Exception as e:
            messages.error(request, 'An Error occured. Try again')

@login_required(login_url='login')
def profile(request,pk):
    profile = Profile.objects.get(id=pk)
    posts = profile.post_set.all()
    businesses = profile.business_set.all()
    form = ProfileForm(instance=profile)
    neighbourhoods = Neighbourhood.objects.all()
    

    if request.method == 'POST':
        try:
            hood_name = request.POST.get('users_neighbourhood')
            hood, created = Neighbourhood.objects.get_or_create(name=hood_name).lower()
            print(hood)

            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.users_neighbourhood = hood
                profile.save()
                messages.success(request, 'Your profile was updated')
                return redirect('profile', pk=pk)
            else:
                messages.error(request, 'Your input(s) was not valid, Try again')
        except Exception as e:
            messages.error(request, 'An Error occured. Try again', print(e), e)

    context={"profile":profile, "posts":posts, "form":form, "neighbourhoods":neighbourhoods, "businesses":businesses}
    return render(request, 'base/profile.html', context)
