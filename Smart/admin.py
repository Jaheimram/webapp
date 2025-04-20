from django.contrib import admin
from .models import TodoItem
from .models import Post
from .models import FAQ
from .models import CaseStudyZip
from .models import TeamMember


# Register your models here.
@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_at')
    list_filter = ('completed', 'user', 'created_at')
    search_fields = ('title',)
    list_editable = ('completed',)
    date_hierarchy = 'created_at'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')  # Fields to display in the list view
    search_fields = ('title', 'content')  # Fields to search by
    list_filter = ('created_at', 'author')  # Filters for the list view

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')

@admin.register(CaseStudyZip)
class CaseStudyZipAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active')
    list_editable = ('order', 'is_active')