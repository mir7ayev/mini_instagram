from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def signup_view(r):
    if r.method == 'POST':
        User.objects.create(username=r.POST['username'],
                            password=make_password(r.POST['password'])).save()

        return redirect('/auth/signin/')

    return render(r, 'signup.html')


def signin_view(r):
    if r.method == 'POST':
        username = r.POST.get('username')
        password = r.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(r, user)
            next_page = r.GET.get('next', '/')

            return redirect(next_page, '/')

        return redirect('/auth/signup/')
    return render(r, 'signin.html')


@login_required(login_url='/auth/signin/')
def logout_view(r):
    logout(r)
    return redirect('/auth/signin/')
