from django.contrib import admin

from .models import Folder, Document, Tag


class FolderAdmin(admin.ModelAdmin):
    list_display = ('label', 'owner', 'is_public', 'date_updated')
    list_editable = ('is_public',)
    list_filter = ('is_public', 'owner__username')
    search_fields = ['label', 'description']
    readonly_fields = ('date_created', 'date_updated')


admin.site.register(Folder, FolderAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public', 'date_updated')
    list_editable = ('is_public',)
    list_filter = ('is_public', 'owner__username')
    search_fields = ['url', 'title', 'description']
    readonly_fields = ('date_created', 'date_updated')


admin.site.register(Document, DocumentAdmin)
admin.site.register(Tag)
