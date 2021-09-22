from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return render(request, "network/index.html")

def posts(request):

    posts = Post.objects.order_by('-timestamp').all()

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return JsonResponse([post.serialize() for post in numbers], safe=False)



def likes(request):
    user = request.user
    liked = Like.objects.filter(user__exact = user)
    lst = []
    for pos in liked:
        lst.append(pos.post.id)    
    return JsonResponse([r for r in lst], status=201, safe=False)



@csrf_exempt
@login_required
def profile(request,name):
    user = User.objects.get(username=name)
    posts = Post.objects.order_by("-timestamp").filter(user=user)

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return JsonResponse([post.serialize() for post in numbers], safe=False)



@csrf_exempt
@login_required
def follow(request, name, boo):
    user = request.user
    if boo==1:
        following = User.objects.get(username=name)
        foll = Follow(user=user, following=following)
        foll.save()
    elif boo==0:
        following = User.objects.get(username=name)
        foll = Follow.objects.get(user=user, following=following)
        foll.delete()
    return JsonResponse({'follow': boo}, status=201) 

@csrf_exempt
@login_required
def followed(request,name):
    user = request.user
    try:
        foll = User.objects.get(username=name)
        following = Follow.objects.get(user=user, following=foll)
        return JsonResponse({'followed': True}, status=201)
    except:
        return JsonResponse({'followed': False}, status=201)


def following(request):
    user = request.user
    followed = Follow.objects.all()
    posts = Post.objects.order_by("-timestamp").all()
    lst = []
    for post in posts:
        for foll in followed:
            if user == foll.user and post.user == foll.following:
                lst.append(post)

    page = request.GET.get('page', 1)

    paginator = Paginator(lst, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    
    return JsonResponse([post.serialize() for post in numbers], safe=False)
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def addpost(request):
    data = json.loads(request.body)
    post = data.get("post")
    user = request.user

    current_post = Post(user=user,post=post)
    current_post.save()

    return JsonResponse(current_post.serialize(), status=201)

@csrf_exempt
@login_required
def addlike(request,id):
    user = request.user
    data = json.loads(request.body)
    active = data.get("active")
    post = Post.objects.get(pk=id)
    if active:
        like = Like(user=user, post=post)
        like.save()
    else:
        like = Like.objects.get(user=user, post=post)
        like.delete()
    return JsonResponse({'active': active},status=201)

@csrf_exempt
@login_required
def getpost(request,ID):
    post = Post.objects.get(pk=ID)
    return JsonResponse(post.serialize(), safe=False)

@csrf_exempt
@login_required
def edit(request, ID):
    data = json.loads(request.body)
    post = data.get('post')
    post = Post.objects.filter(pk=ID).update(post=post)
    return JsonResponse({'post': post}, status=201)


@csrf_exempt
@login_required
def getpage(request):
    data = json.loads(request.body)
    page = data.get('page')

    return JsonResponse({'page':page})

import math

@csrf_exempt
def numpagesP(request):
    posts = Post.objects.all()
    maxpages = math.ceil(len(posts)/10)
    return JsonResponse({'maxpages': maxpages, 'length':len(posts)})


@csrf_exempt
@login_required
def numpagesF(request):
    user = request.user
    followed = Follow.objects.all()
    posts = Post.objects.order_by("-timestamp").all()
    lst = []
    for post in posts:
        for foll in followed:
            if user == foll.user and post.user == foll.following:
                lst.append(post)

    maxpages = math.ceil(len(lst)/10)

    return JsonResponse({'maxpages': maxpages, 'length':len(lst)})


@csrf_exempt
@login_required
def numpagesU(request,name):
    user = User.objects.get(username=name)
    posts = Post.objects.order_by("-timestamp").filter(user=user)
    maxpages = math.ceil(len(posts)/10)
    return JsonResponse({'maxpages': maxpages, 'length':len(posts)})

@csrf_exempt
@login_required
def getfollow(request,name):
    user = User.objects.get(username=name)
    foll = Follow.objects.filter(user=user)
    fell = Follow.objects.filter(following=user)

    return JsonResponse({'following': len(foll), 'followers':len(fell)  })



