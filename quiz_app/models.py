from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    """Model for Quiz"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_questions_count(self):
        return self.questions.count()


class Question(models.Model):
    """Model for Question"""
    QUESTION_TYPES = [
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='single')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"


class Answer(models.Model):
    """Model for Answer options"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"


class UserSubmission(models.Model):
    """Model for User Quiz Submission"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    user_name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user_name} - {self.quiz.title} - Score: {self.score}"

    def calculate_percentage(self):
        total_questions = self.quiz.questions.count()
        if total_questions > 0:
            return (self.score / total_questions) * 100
        return 0


class UserAnswer(models.Model):
    """Model for individual answers in a submission"""
    submission = models.ForeignKey(UserSubmission, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submission.user_name} - Q: {self.question.id}"


class Event(models.Model):
    """Model for Events"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def is_upcoming(self):
        return self.date >= timezone.now()