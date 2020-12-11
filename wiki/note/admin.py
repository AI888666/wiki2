from django.contrib import admin
from note.models import Note


# Register your models here.
class NoteManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_time', 'updated_time', 'user', 'is_active']
    list_display_links = ['title']
    search_fields = ['title']


admin.site.register(Note, NoteManager)

