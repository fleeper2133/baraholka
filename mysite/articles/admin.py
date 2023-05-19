from django.contrib import admin
from .models import *


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'acceptance_stage', 'photo', 'user', 'cat')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('acceptance_stage',)
    list_filter = ('time_create',)


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Category)

