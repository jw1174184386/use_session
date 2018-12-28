from django.db import models
from django import forms


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    #  验证登录账户
    token = models.CharField(max_length=64, editable=False, default="")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
