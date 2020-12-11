from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import User
import hashlib


# Create your views here.
def reg_view(request):
    if request.method == "GET":
        # 返回页面
        return render(request, 'user/reg.html')

    elif request.method == "POST":
        # 处理数据
        username = request.POST.get("username")
        password_1 = request.POST.get("password_1")
        password_2 = request.POST.get("password_2")
        # TODO 参数检查
        if username == "" or password_1 == "":
            error = "用户名或密码不能为空！"
            return render(request, 'user/reg.html', locals())

        if password_1 != password_2:
            error = "两次密码不一致！"
            return render(request, 'user/reg.html', locals())

        # objects.get ->obj---try except
        # objects.filter -> QuerySet
        old_users = User.objects.filter(username=username, is_active=True)
        if old_users:
            error = "用户名已存在！"
            return render(request, 'user/reg.html', locals())
        # 密码
        # 哈希(hash)算法(md5, sha-1, sha-256...)
        # 特点：1、md5:定长出入，2、不可逆，
        # 3、雪崩效应--文件完整性(20G)--分段（抽样）计算比对hash值
        m = hashlib.md5()   # 获取计算对象
        m.update(password_1.encode())  # 更新明文
        password_h = m.hexdigest()  # 获取16进制结果

        # 创建用户，设置unique=True唯一标识，多个用户同时创建用户时，会重复插入
        try:
            user = User.objects.create(username=username, password=password_h)
        except Exception as e:
            print(e)
            error = "用户名重复插入，请重新输入！"
            return render(request, 'user/reg.html', locals())

        # user = User.objects.all().update(username=F('username')+1)

        # 注册成功后，免登录一天
        request.session['username'] = username

        # return HttpResponse("---reg----")
        return HttpResponseRedirect("/user/login")

    return HttpResponse("---Your method is wrong---")


def login_view(request):
    if request.method == "GET":
        # 检查登录状态
        # 1、检查session
        if "username" in request.session:
            username = request.session["username"]
            print(username)
            # return HttpResponse("---已登录---")
            # return redirect("/note/", {"username": username})
            return HttpResponseRedirect("/note/", {"name": username})

        # 2、检查cookies[有数据记得会写session]
        if "username" in request.COOKIES:
            username = request.COOKIES["username"]
            request.session["username"] = username
            # return HttpResponse("=====已登录====")
            # return redirect("/note/", {"username": username})
            print(username)
            return HttpResponseRedirect("/note/", {"name": username})

        return render(request, 'user/login.html')

    elif request.method == "POST":
        # 检验用户名、密码，保存会话状态
        username = request.POST.get("username")
        password = request.POST.get("password")

        users = User.objects.filter(username=username, is_active=True)

        if username == "" or password == "":
            error = "用户名或密码不能为空！"
            return render(request, "user/login.html", locals())

        if not users:
            error = "用户名不正确！"
            return render(request, "user/login.html", locals())

        # username唯一约束，所有username查询，如果有结果，
        # 一定是QuerySet里的第一个元素
        user = users[0]

        m = hashlib.md5()
        m.update(password.encode())
        c_password = m.hexdigest()

        if c_password != user.password:
            error = "密码不正确！"
            return render(request, "user/login.html", locals())

        # resp = HttpResponse("登录成功！")
        # resp = redirect("/note/", {"username": username})
        print(username)
        resp = HttpResponseRedirect("/note/", {"name": username})
        # resp = render(request, "user/index.html", locals())
        # 保持状态
        request.session['username'] = username
        # 是否保存Cookies,取决于用户是否点击了checkbox
        if "long" in request.POST:
            resp.set_cookie("username", username, 60 * 60 * 24 * 20)
        return resp

    return HttpResponse("Your method is wrong")


def logout_view(request):
    return render(request, "index/index.html")