from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizResult

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = int(request.POST.get(f'question_{question.id}'))
            if user_answer == question.correct_option:
                score += 1
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
        return render(request, 'quiz_result.html', {'score': score, 'quiz': quiz})

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})
