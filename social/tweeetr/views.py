from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweeet
from .forms import Tweeet_form, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        form = Tweeet_form(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweeet = form.save(commit=False)
                tweeet.user = request.user
                tweeet.save()
                messages.success(request, "your tweeet has been posted")
                return redirect('home')
        user_profile = Profile.objects.get(user=request.user)
        tweeets = Tweeet.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'tweeets':tweeets, "form":form})
    else:
     tweeets = Tweeet.objects.all().order_by('-created_at')
     return render(request, 'home.html', {'tweeets':tweeets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, "login to view this page")
        return redirect('home')


def followers(request, pk):
        if request.user.is_authenticated and request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles": profiles})
        else:
            messages.success(request, "Ooops, this is not your profile!!")
            return redirect('home')


def following(request, pk):
    if request.user.is_authenticated and request.user.id == pk:
        profiles = Profile.objects.get(user_id=pk)
        return render(request, 'following.html', {"profiles": profiles})
    else:
        messages.success(request, "Ooops, this is not your profile!!")
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, (f"You have unfollowed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "login to view this page")
        return redirect('home')


def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request, (f"You have followed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "login to view this page")
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:

        profile = Profile.objects.get(user_id=pk)
        tweeets= Tweeet.objects.filter(user_id=pk)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'profile.html', {'profile':profile, 'tweeets':tweeets})

    else:
        messages.success(request, "login to view this page")
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "you have successfully logged in")
            return redirect('home')
        else:
            messages.success(request, "there was an error. Try again")
            redirect('login')
    else:
        return render(request, "login.html", {})
    return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out")

    return render(request, 'home.html', {})


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # login user
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "Registration successful. Welcome!")
            return redirect('home')

    return render(request, 'register.html', {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        profile_user = Profile.objects.get(user__id=request.user.id)
        current_user = User.objects.get(id=request.user.id)
        profile_pic_form = ProfilePicForm(request.POST or None,request.FILES or None, instance=profile_user)
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        if user_form.is_valid() and profile_pic_form.is_valid():
            user_form.save()
            profile_pic_form.save()
            login(request, current_user)
            messages.success(request, "Your profile has been updated")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, 'profile_pic_form':profile_pic_form})
    else:
        messages.success(request, "Log in to update your profile!")
        return redirect('home')


def tweeet_like(request, pk):
    if request.user.is_authenticated:
        tweeet = get_object_or_404(Tweeet, id=pk)
        if tweeet.likes.filter(id=request.user.id):
            tweeet.likes.remove(request.user)
        else:
            tweeet.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "Log in to like tweeets!")
        return redirect('home')


def show_tweeet(request, pk):
    tweeet = get_object_or_404(Tweeet, id=pk)
    if tweeet:
        return render(request, 'show_tweeet.html', {'tweeet':tweeet})
    else:
        messages.success(request, "That tweeet does not exist!")
        return redirect('home')


def delete_tweeet(request, pk):
    if request.user.is_authenticated:
        tweeet = get_object_or_404(Tweeet, id=pk)
        if request.user.id == tweeet.user.id:
            messages.success(request, "your tweeet has been deleted")
            tweeet.delete()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "thats not your tweeet")
            return redirect('home')
    else:
        messages.success(request, "Log in to like tweeets!")
        return redirect('home')


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        searched = Tweeet.objects.filter(body__contains = search)
        return render(request, 'search.html', {'search':search, 'searched':searched})

    else:
        return render(request, 'search.html', {})


def search_users(request):
    if request.method == 'POST':
        search = request.POST['search']
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_users.html', {'search':search, 'searched':searched})

    else:
        return render(request, 'search_users.html', {})

