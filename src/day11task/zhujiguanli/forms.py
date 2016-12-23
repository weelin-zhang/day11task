#_*_coding:utf-8_*_
'''
Created on 2016年11月20日

@author: ZWJ
'''
from django import forms
from logging import PlaceHolder
class RegisterUserForm(forms.Form):
    username = forms.CharField(min_length=6,widget=forms.TextInput({ "placeholder": "username"}))
    password = forms.CharField(widget=forms.PasswordInput({ "placeholder": "password"}),min_length=6)
    email = forms.EmailField(widget=forms.EmailInput({ "placeholder": "xxxx@xxx"}))
    phone = forms.CharField(min_length=11,max_length=11,widget=forms.NumberInput({ "placeholder": "11111111111"}))
    
class LoginForm(forms.Form):
    username = forms.CharField(min_length=6,error_messages={'required':('用户名不能为空'),'invalid':('用户名格式不正确..')},widget=forms.TextInput({ "placeholder": "username"}))
    password = forms.CharField(widget=forms.PasswordInput({ "placeholder": "password"}))
    
