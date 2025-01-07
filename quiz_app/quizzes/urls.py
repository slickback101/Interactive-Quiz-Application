from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quizzes/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('result/', views.result, name='result'),
    path('admin/', admin.site.urls),
    path('', include('quizzes.urls')),  # Include the quizzes app URLs
]
