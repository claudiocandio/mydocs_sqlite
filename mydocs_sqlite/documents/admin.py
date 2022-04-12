from django.contrib import admin

from documents.models import Document, Owner, Category, File, MyDocsSettings


class FileInline(admin.TabularInline):
    model = File

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'owners', 'categories', 'date')
    search_fields = ('document_name', 'date', 'owner__name', 'category__name')
    list_filter = ('owner','category','date')
    
    filter_horizontal = ('owner', 'category',)
    #filter_vertical = ('owner', 'category',)

    # to show files in doc, not working well as files are in db    
    #inlines = [FileInline]

    #fieldsets = [
    #    ('Field New Name',{fields:[document_name]}),
    #]

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address')
    search_fields = ('name', 'email', 'address')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class FileAdmin(admin.ModelAdmin):
    list_display = ('document', 'file_name', 'file_date', 'file_size', 'file_type')
    search_fields = ('document', 'file_name', 'file_date', 'file_type')
    list_filter = ('file_type', 'file_date')

admin.site.register(Document, DocumentAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(MyDocsSettings)


