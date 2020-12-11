from django.conf.urls import url

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/note/
    url(r"^$", views.index_view),
    # http://127.0.0.1:8000/note/list_note
    url(r"^list_note$", views.list_note, name='list_note'),
    # http://127.0.0.1:8000/note/add_note
    url(r"^add_note$", views.add_view, name='add_note'),
    # http://127.0.0.1:8000/note/mod/2
    url(r"^mod/(\d+)$", views.mod_view),
    # http://127.0.0.1:8000/note/del/6
    url(r"^del/(\d+)$", views.del_view),
    # http://127.0.0.1:8000/note/del/6
    url(r"^(\d+)$", views.show_view),
]
