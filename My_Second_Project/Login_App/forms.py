from django import forms
from django.contrib.auth.models import User
from Login_App.models import userinfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class UserInfoForm(forms.ModelForm):
    class Meta():
        model = userinfo
        fields = ('facebook_id','profile_pic')
