from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
import os

# Create your views here.

def home(request):
    un = request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        tweets = Tweet.objects.all()
        d = {'tweets': tweets, 'UO': UO}
        return render(request, 'home.html', d)
    tweets = Tweet.objects.all()
    d = {'tweets': tweets}
    return render(request, 'home.html', d)

def register(request):
    ERFO = UserForm()
    d = {'ERFO': ERFO}
    if request.method == 'POST':
        UFDO = UserForm(request.POST)
        if UFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            return HttpResponseRedirect(reverse('user_login'))
        return HttpResponse('Invalid Data')
    return render(request, 'register.html', d)

def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('Invalid Credentials')
    return render(request, 'user_login.html')




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

# today 27/08/2024
@login_required
def create_tweet(request):
    ETFO = TweetForm()
    d = {'ETFO': ETFO}
    if request.method == 'POST' and request.FILES:
        TFDO = TweetForm(request.POST, request.FILES)
        un = request.session.get('username')
        UO = User.objects.get(username=un)
        if UO:
            MTFDO = TFDO.save(commit=False)
            MTFDO.username = UO
            MTFDO.save()
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('Invalid Info')
    return render(request, 'create_tweet.html', d)


@login_required
def update(request, pk):
    TO = Tweet.objects.get(pk=pk)
    d = {'TO':TO}
    if request.method == 'POST' and request.FILES:
        if TO.photo:
            os.remove(TO.photo.path)
        TO.text = request.POST.get('text')
        TO.photo = request.FILES.get('photo')
        TO.save()
        return HttpResponse('Done')
    return render(request, 'update.html', d)


@login_required
def delete(request, pk):
    TO = Tweet.objects.get(pk=pk)
    if TO.username.username == request.session.get('username'):
        TO.delete()
        return HttpResponseRedirect(reverse('home'))
    return HttpResponse("You can't Delete some others Tweet")
# Create your views here.
def save(request, pk):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    TO = Tweet.objects.get(pk =pk)
    ASTO = Saved.objects.filter(tweet=TO)

    if ASTO and ASTO[0].username.username == un:
        ASTO.delete()
        return HttpResponseRedirect(reverse('saved')) 
    else:
        if TO.username.username != request.session.get('username'):
            STO = Saved(username=UO, tweet=TO)
            STO.save()
            return HttpResponseRedirect(reverse('saved'))
    return HttpResponse('You can"t Save Your Tweets' )


def saved(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    saved_tweets = Saved.objects.filter(username=UO)
    d = {'tweets' : saved_tweets}
    return render(request, 'saved.html',d)