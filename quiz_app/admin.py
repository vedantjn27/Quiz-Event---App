from django.contrib import admin
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


class AnswerInline(admin.TabularInline):
    """Inline admin for answers"""
    model = Answer
    extra = 4
    fields = ['text', 'is_correct']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin for Question model"""
    list_display = ['text', 'quiz', 'question_type', 'created_at']
    list_filter = ['quiz', 'question_type', 'created_at']
    search_fields = ['text', 'quiz__title']
    inlines = [AnswerInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin for Quiz model"""
    list_display = ['title', 'get_questions_count', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin for Answer model"""
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['text', 'question__text']


class UserAnswerInline(admin.TabularInline):
    """Inline admin for user answers"""
    model = UserAnswer
    extra = 0
    readonly_fields = ['question', 'answer', 'is_correct']
    can_delete = False


@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    """Admin for UserSubmission model"""
    list_display = ['user_name', 'quiz', 'score', 'submitted_at']
    list_filter = ['quiz', 'submitted_at']
    search_fields = ['user_name', 'quiz__title']
    readonly_fields = ['submitted_at']
    inlines = [UserAnswerInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin for Event model"""
    list_display = ['title', 'date', 'location']
    list_filter = ['date']
    search_fields = ['title', 'description', 'location']
    ordering = ['date']