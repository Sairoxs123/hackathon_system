from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Users)

class UsersAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "grade_sec"]
    ordering = ["id"]
    search_fields = ["name", "email"]
    list_filter = ["grade_sec"]

@admin.register(Submissions)

class SubmissionsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "submit_time", "exec_time", "correct"]
    ordering = ["submit_time"]
    search_fields = ["user"]
    list_filter = ["user"]

@admin.register(Questions)

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "question", "inputs", "outputs", "difficulty"]
    ordering = ["id"]
    search_fields = ["id", "title", "question"]
    list_filter = ["difficulty"]

@admin.register(CodeStorage)

class CodeStorageAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "question"]
    ordering = ["id"]
    search_fields = ["user", "question"]
    list_filter = ["question"]

@admin.register(Competition)

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ["session_code", "start", "end"]
    ordering = ["session_code"]
    search_fields = ["session_code"]

@admin.register(CompSubmissions)

class CompSubmissionsAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "submit_time", "exec_time", "memory", "correct", "barred"]
    ordering = ["id"]
    search_fields = ["question"]

@admin.register(CompCodeStorage)

class CompCodeStorageAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "user"]
    ordering = ["id"]
    search_fields = ["question", "user"]
