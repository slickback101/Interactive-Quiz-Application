from django.urls import path
from .views import QuizListAPI

urlpatterns = [
    path('api/quizzes/', QuizListAPI.as_view(), name='quiz_list_api'),
]
