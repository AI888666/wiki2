from django.contrib import admin
from user.models import User
from note.models import Note


# Register your models here.
class UserManager(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'created_time', 'updated_time', 'is_active']
    list_display_links = ['username']
    search_fields = ['username']


# class NoteManager(admin.ModelAdmin):
#     list_display = ['id', 'title', 'content', 'created_time', 'updated_time', 'user']
#     list_display_links = ['title']
#     search_fields = ['title']


admin.site.register(User, UserManager)
# admin.site.register(Note, NoteManager)
