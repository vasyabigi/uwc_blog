from django.contrib import admin
from models import Category, Post, Tag, PostComment


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Tag, TagAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status')
    list_filter = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Post, PostAdmin)


class PostCommentAdmin(admin.ModelAdmin):
    list_filter = ('post',)
admin.site.register(PostComment, PostCommentAdmin)
