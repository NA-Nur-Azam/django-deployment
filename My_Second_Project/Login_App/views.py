from django.shortcuts import render
from Login_App.forms import UserForm,UserInfoForm
from Login_App.models import userinfo
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def login_page(request):
    return render(request,'Login_App/login.html',context={})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('LoginApp:index'))
            else:
                return HttpResponse("Account is not actived!")
        else:
            return HttpResponse("Login details is Wrong!")
    else:
        #return render(request, 'Login_App/login.html', context={})
        return HttpResponseRedirect(reverse('LoginApp:login'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('LoginApp:logout'))

def index(request):
    dict = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = userinfo.objects.get(user__pk=user_id)
        dict = {'user_basic_info':user_basic_info,'user_more_info':user_more_info,}
    return render(request,'Login_App/index.html',context=dict)

def register(request):

    registered = False

    if request.method == 'POST':
        User_Form  = UserForm(data=request.POST)
        User_Info_Form = UserInfoForm(data=request.POST)

        if User_Form.is_valid() and User_Info_Form.is_valid():
            user = User_Form.save()
            user.set_password(user.password)
            user.save()

            User_Info = User_Info_Form.save(commit=False)
            User_Info.user = user

            if 'profile_pic' in request.FILES:
                User_Info.profile_pic = request.FILES['profile_pic']

            User_Info.save()
            registered = True
    else:
        User_Form = UserForm()
        User_Info_Form = UserInfoForm()
    dict = {'User_Form':User_Form,'User_Info_Form':User_Info_Form,'registered':registered}
    return render(request,'Login_App/register.html',context=dict)
