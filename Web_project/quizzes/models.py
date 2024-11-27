from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис категорії")

    def __str__(self):
        return self.name


class Quiz(models.Model):
    DIFFICULTY_LEVELS = [
        ('easy', 'Легкий'),
        ('medium', 'Середній'),
        ('hard', 'Складний'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes', verbose_name="Категорія")
    name = models.CharField(max_length=200, verbose_name="Назва вікторини")
    description = models.TextField(blank=True, verbose_name="Опис вікторини")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, verbose_name="Рівень складності")

    def __str__(self):
        return f"{self.name} ({self.get_difficulty_display()})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name="Вікторина")
    text = models.TextField(verbose_name="Текст питання")
    points = models.PositiveIntegerField(verbose_name="Бали за правильну відповідь", default=0)

    def save(self, *args, **kwargs):
        # Призначаємо бали автоматично залежно від складності вікторини
        if self.quiz.difficulty == 'easy':
            self.points = 4
        elif self.quiz.difficulty == 'medium':
            self.points = 7
        elif self.quiz.difficulty == 'hard':
            self.points = 10
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Питання")
    text = models.CharField(max_length=200, verbose_name="Текст відповіді")
    is_correct = models.BooleanField(default=False, verbose_name="Чи правильна відповідь")

    def __str__(self):
        return self.text

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results', verbose_name="Користувач")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results', verbose_name="Вікторина")
    score = models.PositiveIntegerField(verbose_name="Бали")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата проходження")

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name} - {self.score} балів"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)  # Поле для хранения ранга

    def __str__(self):
        return self.user.username