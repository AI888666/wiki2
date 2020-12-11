from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from user.models import User
from .models import Note


# Create your views here.
def check_login(fn):
    # 装饰器
    def wrap(request, *args, **kwargs):
        if "username" not in request.session:
            # Cookies
            if "username" not in request.COOKIES:
                return HttpResponseRedirect("/user/login")
            else:
                # 回写session
                username = request.COOKIES["username"]
                request.session["username"] = username
            user = User.objects.get(username=username)
            request.my_user = user
        return fn(request, *args, **kwargs)
    return wrap


@check_login
def index_view(request):
    user = request.my_user
    username = user.username
    return render(request, 'note/index_note.html', locals())


@check_login
def list_note(request):
    note = Note.objects.all().filter(is_active=True)
    paginator = Paginator(note, 3)
    print('当前对象的总个数：', paginator.count)
    print('当前对象的页码的范围：', paginator.page_range)
    print('总页数：', paginator.num_pages)
    print('每页最大个数：', paginator.per_page)

    cur_page = request.GET.get('page', 1)  # 获取默认的当前页
    page = paginator.page(cur_page)

    return render(request, 'note/list_note.html', locals())


@check_login
def add_view(request):
    if request.method == "GET":
        return render(request, "note/add_note.html")

    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        number = request.POST.get("username")
        try:
            note = Note.objects.get(title=title, is_active=True)
        except Exception as e:
            print(e)
            note = Note.objects.create(title=title, content=content, user_id=number)
            return HttpResponseRedirect("/note/list_note")
        if note:
            error_msg = "你要添加的笔记已经存在!"
            return render(request, "note/add_note.html", locals())
    return HttpResponse("Your method is wrong!")


@check_login
def mod_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id, is_active=True)
    except Exception as e:
        print(e)
        return HttpResponse("You note id is wrong or note is delete!")

    if request.method == "GET":
        return render(request, "note/mod_note.html", locals())

    elif request.method == "POST":
        # 更新
        content = request.POST.get("content")
        # TODO 检验数据是否存在
        to_update = False
        if content != note.content:
            to_update = True
        if to_update:
            note.content = content
            note.save()
        return HttpResponseRedirect("/note/list_note")


@check_login
def del_view(request, id):
    note01 = Note.objects.filter(id=id, is_active=True)
    if not note01:
        return HttpResponse("你要删除的笔记没有!")
    # 因为查找时，按主键查询，所以QuerySet如果有值，必然是只有一个
    note01 = note01[0]
    note01.is_active = False
    note01.save()
    return HttpResponseRedirect("/note/list_note")


@check_login
def show_view(request, id):
    if request.method == "GET":
        note1 = Note.objects.filter(id=id, is_active=True)
        return render(request, "note/note.html", locals())
    else:
        return HttpResponse("显示有误!")

