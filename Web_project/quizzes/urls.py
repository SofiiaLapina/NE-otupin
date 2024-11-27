from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.select_difficulty, name='select_difficulty'),
    path('categories/<int:category_id>/<str:difficulty>/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),  # Новий маршрут
    path('quiz/<int:quiz_id>/question/<int:question_number>/', views.quiz_question, name='quiz_question'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:quiz_id>/complete/', views.quiz_complete, name='quiz_complete'),  # Новий маршрут
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
