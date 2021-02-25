from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):  # title로 todo 검색
    search_fields = ['title']


admin.site.register(Todo, TodoAdmin)