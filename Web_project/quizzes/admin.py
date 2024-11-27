from django.contrib import admin
from .models import Category, Quiz, Question, Answer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty')
    list_filter = ('category', 'difficulty')
    search_fields = ('name',)

class AnswerInline(admin.TabularInline):
    model = Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'points')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [AnswerInline]
