from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Quiz, Answer
from django.http import JsonResponse
from .models import QuizResult
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def select_difficulty(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    difficulties = ['easy', 'medium', 'hard']
    return render(request, 'select_difficulty.html', {'category': category, 'difficulties': difficulties})
def leaderboard(request):
    leaderboard_data = (
        QuizResult.objects.values('user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:10]  # Топ 10 користувачів
    )
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard_data})
def quiz_list(request, category_id, difficulty):
    category = get_object_or_404(Category, pk=category_id)
    quizzes = Quiz.objects.filter(category=category, difficulty=difficulty)
    return render(request, 'quiz_list.html', {'category': category, 'difficulty': difficulty, 'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})

@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    request.session['quiz_score'] = 0
    return redirect('quiz_question', quiz_id=quiz.id, question_number=1)

def quiz_question(request, quiz_id, question_number):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()  # Отримуємо всі питання для вікторини

    # Перевіряємо, чи є питання в межах вікторини
    if question_number > questions.count():
        return redirect('quiz_complete', quiz_id=quiz.id)

    question = questions[question_number - 1]  # Питання для поточного номера

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        if not selected_answer_id:
            return render(request, 'quiz_question.html', {
                'quiz': quiz,
                'question': question,
                'question_number': question_number,
                'total_questions': questions.count(),
                'error': 'Ви повинні обрати відповідь!'
            })

        # Перевіряємо, чи відповідь правильна
        try:
            selected_answer = Answer.objects.get(pk=selected_answer_id, question=question)
            if selected_answer.is_correct:
                # Додаємо бали до сесії
                score = request.session.get('quiz_score', 0)
                score += question.points
                request.session['quiz_score'] = score
        except Answer.DoesNotExist:
            pass

        # Перехід до наступного питання
        return redirect('quiz_question', quiz_id=quiz.id, question_number=question_number + 1)

    # Відображаємо поточне питання
    return render(request, 'quiz_question.html', {
        'quiz': quiz,
        'question': question,
        'question_number': question_number,
        'total_questions': questions.count(),
    })

def quiz_complete(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    score = request.session.get('quiz_score', 0)

    # Збереження результатів для авторизованого користувача
    if request.user.is_authenticated:
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score)

    # Очищення сесії
    request.session.pop('quiz_score', None)

    return render(request, 'quiz_complete.html', {'quiz': quiz, 'score': score})