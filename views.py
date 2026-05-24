from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from .forms import TweetForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')



def user_logout(request):
    logout(request)
    return redirect('login')   

def tweet_list(request):
    tweets = Tweet.objects.select_related('user').order_by('-created_at')
    form = TweetForm()
    context = {'tweets': tweets, 'form': form}
    return render(request, 'tweet/tweet_list.html', context)

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Tweet created.")
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet/tweet_create.html', {'form': form})

@login_required
def tweet_edit(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this tweet.")
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Tweet updated.")
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet/tweet_edit.html', {'form': form, 'tweet': tweet})

@login_required
def tweet_delete(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.user != request.user:
        return HttpResponseForbidden("You cannot delete this tweet.")
    if request.method == 'POST':
        tweet.delete()
        messages.success(request, "Tweet deleted.")
        return redirect('tweet_list')
    return render(request, 'tweet/tweet_confirm_delete.html', {'tweet': tweet})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registered and logged in.")
            return redirect('tweet_list')
    else:
        form = RegisterForm()
    return render(request, 'tweet/register.html', {'form': form})

