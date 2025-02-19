from tkinter import Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    email = forms.CharField(label='شماره تماس', widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    first_name = forms.CharField(label='نام', max_length=50, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(label='نام خانوادگی', max_length=50, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    password1 = forms.CharField(label='کلمه عبور', widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    password2 = forms.CharField(label='تکرار کلمه عبور', widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super(RegisterUserForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'
        



