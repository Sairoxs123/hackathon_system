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
    list_display = ["id", "user", "submit_time", "exec_time", "memory", "correct"]
    ordering = ["submit_time"]
    search_fields = ["user"]
    list_filter = ["user"]

@admin.register(Questions)

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "question", "inputs", "outputs", "difficulty", "points"]
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

@admin.register(Quiz)

class QuizzesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "single_submit"]
    ordering = ["id"]
    search_fields = ["title"]

@admin.register(QuizSubmissions)

class QuizSubmissionsAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "question", "correct", "submit_time"]
    ordering = ["id"]
    search_fields = ["student", "question"]
    list_filter = ["question", "student"]

@admin.register(Question)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "quiz", "text"]
    ordering = ["id"]
    search_fields = ["quiz", "text"]
    list_filter = ["quiz"]

@admin.register(Option)

class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "text", "is_correct"]
    ordering = ["id"]
    search_fields = ["question", "text"]
    list_filter = ["question"]

@admin.register(Updates)

class UpdatesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "date"]
    ordering = ["id"]
    search_fields = ["title", "description"]
    list_filter = ["date"]