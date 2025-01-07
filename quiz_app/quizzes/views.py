from django.shortcuts import render
from .models import Quiz
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from .serializers import QuizSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/home.html', {'quizzes': quizzes})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'quizzes/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'quizzes/login.html', {'error': 'Invalid credentials'})
    return render(request, 'quizzes/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


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
        return redirect('result')

    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})


def result(request):
    result = QuizResult.objects.filter(user=request.user).last()
    return render(request, 'quizzes/result.html', {'result': result})


class QuizListAPI(APIView):
    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
