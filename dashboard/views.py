# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import SignUpForm
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('search:index'))
    return render(request, 'dashboard/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('search:index'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
