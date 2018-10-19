#!/usr/bin/env python
#coding:utf8

from forms import LoginForm
from django.shortcuts import render
from django.contrib import auth
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from asset.models import PhysicalServer, IDC, Asset
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    idc_number = IDC.objects.aggregate(idc_number=Count('name'))['idc_number']
    ps_number = PhysicalServer.objects.aggregate(ps_number=Count('sn'))['ps_number']
    host_number = Asset.objects.aggregate(host_number=Count('asset_type'))['host_number']
    online_user = request.user.username
    return render(request, 'index.html', locals())

def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if not user:
                error = 'Invalid user or incorrect password.'
                messages.add_message(request, messages.ERROR, error)
                return HttpResponseRedirect(reverse('loginview'))
            elif not user.is_staff:
                error = 'user {0} is not allow logged in.'.format(username)
                messages.add_message(request, messages.ERROR, error)
                return HttpResponseRedirect(reverse('loginview'))
            else:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    form = LoginForm()
    return render(request, 'registration/login.html', locals())

def logoutview(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
