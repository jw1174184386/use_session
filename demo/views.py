from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from demo.models import *


#  定义一个装饰器

def check_login(func):
    def check(request, *args, **kwargs):
        username = request.session.get('username', None)
        if username:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('demo:login'))
    return check


def register(request):
    return HttpResponse("register")


def login(request):
    if request.method == "GET":
        u_token = request.COOKIES.get('u_token', None)
        if u_token:
            # 验证
            user = User.objects.all().filter(token=u_token).first()
            if user:
                # s说明token还有效
                # 自动登录 账号和密码 --- session  所有涉及到的的登录验证都需要取出session
                session = request.session
                session['username'] = user.username
                session['password'] = user.password
                return redirect(reverse('demo:main'))
            else:
                error_message = "MMP,token已经失效了"
                form = UserForm()
                return render(request, 'login.html', locals())
        else:
            # 没有token 不进行自动登录操作
            return render(request, 'login.html')
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # 查找数据中是否存在此用户名
            user = User.objects.all().filter(username=cleaned_data['username']).first()
            if user:
                # 继续判断 判断输入的密码是否和数据库密码相等
                if user.password == cleaned_data['password']:
                    # 验证成功
                    # 跳转到另一个页面 保存数据  自动登录就是将session的数据取出来
                    session = request.session
                    session['username'] = user.username
                    session['password'] = user.password
                    #  设置session的过期时间
                    session.set_expiry(60)
                    # 跳转到首页  区分重定向和转发, 使用重定向到一个试图函数  反向解析地址
                    response = redirect(reverse('demo:main'))
                    # 将token放在cookie中返回给客户端
                    response.set_cookie(key='u_token', value=user.token, max_age=60)
                    return response
                else:
                    error_message = "密码错误"
                    return render(request, 'login.html', locals())
            else:
                error_message = "账号不存在"
                return render(request, 'login.html', locals())
        else:
            error_message = "填写格式错误"
            return render(request, 'login.html', locals())


def main(request):
    return render(request, 'login.html', locals())
