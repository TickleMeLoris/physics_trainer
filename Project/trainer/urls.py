from django.urls import path
from . import views

urlpatterns = [
    path('problem/<int:pk>/', views.problem_detail, name='problem-detail'),
    path('test/start/', views.start_test, name='start-test'),
    path('test/<int:session_id>/<int:problem_num>/', views.test_problem, name='test-problem'),
    path('test/result/<int:session_id>/', views.test_result, name='test-result'),
]