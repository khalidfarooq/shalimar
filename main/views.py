from django.shortcuts import render, redirect
import requests
import api.file_crypto as fc

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from django.contrib.auth.decorators import login_required

from allauth.account.decorators import verified_email_required




def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'B'



@login_required(login_url='/login')
def home(request):
    return render(request, 'main/home.html', {'is_Auth': request.user.is_authenticated})

@login_required(login_url='/login')
def drive_page(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    print(profile)
    x = requests.get('http://127.0.0.1:3000/api/file',
    params={'profile': profile.id, 'is_Auth': request.user.is_authenticated})
    files = x.json()
    for file in files:
        size = format_bytes(file['file_size'])
        temp = file['created_at'][0:10]
        temp = temp.split('-')
        temp = temp[::-1]
        temp = '/'.join(temp)
        file['created_at'] = temp
        file['file_size'] = str("{:.2f}".format(size[0])) + " " + str(size[1])
    context = {'user': user, 'profile': profile, 'files': files, 'is_Auth': request.user.is_authenticated}
    return render(request, 'main/drive.html', context)




@login_required(login_url='/login')
def profile(request):

    user = request.user
    profile = Profile.objects.filter(user=user)[0]
    
    x = requests.get('http://127.0.0.1:3000/api/file',
                    params={'profile': profile.id, 'is_Auth': request.user.is_authenticated})
    files = x.json()
    
    total_file_size=0
    for file in files:
        total_file_size += file['file_size']
    
    total_file_size=format_bytes(total_file_size)
    
    total_file_size=str(round(total_file_size[0],2))+total_file_size[1]
    
    context = {'user': user, 'profile': profile, 'is_Auth': request.user.is_authenticated,'file_length': len(files), 'total_file_size': total_file_size}
    return render(request, 'main/profile.html', context)



def delete_file(request, id):
    x = requests.delete('http://127.0.0.1:3000/api/file/'+id)

    return redirect('/drive')


def view_file(request, id):

    x = requests.get('http://127.0.0.1:3000/api/file/'+id)
    file = x.json()
    data = file['file_data'][2:-1].encode('utf-8')

    user = request.user
    profile = Profile.objects.filter(user=user).first()
    print(profile, profile.cryptoKey)
    profilekey = bytes(profile.cryptoKey[2:-1], 'utf-8')

    decrypted = fc.decrypt(data, profilekey)
    
    return HttpResponse(decrypted, content_type=file['file_content_type'])


@csrf_protect
def register(request):
    if request.method == 'POST':
        data = request.POST
        user = User.objects.create_user(username=data['username'], email=data['email'],
                                        password=data['password'], first_name=data['first_name'], last_name=data['last_name'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        user = authenticate(
            request, username=data['username'], password=data['password'])
        djangoLogin(request, user)
        return redirect('/drive')
    return render(request, 'main/login.html')


@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            djangoLogin(request, user)
            return redirect('/drive')
        else:
            return redirect('/login')
    
    return render(request, 'main/login.html')


def logout(request):
    djangoLogout(request)
    return redirect("/")