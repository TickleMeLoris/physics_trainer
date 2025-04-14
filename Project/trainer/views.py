from django.utils import timezone  
from .models import Problem
from django.http import HttpResponse
from sympy import sympify, Eq
from sympy.parsing.sympy_parser import parse_expr
from .models import TestSession, UserAnswer
import random
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestConfigForm


def check_answer(user_answer, correct_answer):
    try:
        user_expr = parse_expr(user_answer.replace('^', '**'))
        correct_expr = parse_expr(correct_answer.replace('^', '**'))
        return user_expr.equals(correct_expr)
    except:
        return False

def problem_detail(request, pk):
    try:
        # Получаем задачу или возвращаем 404
        problem = get_object_or_404(Problem, pk=pk)
        
        # Получаем соседние задачи для навигации
        prev_problem = Problem.objects.filter(id__lt=pk).order_by('-id').first()
        next_problem = Problem.objects.filter(id__gt=pk).order_by('id').first()
        
        # Обязательно возвращаем HttpResponse
        return render(request, 'trainer/problem.html', {
            'problem': problem,
            'prev_problem': prev_problem,
            'next_problem': next_problem
        })
        
    except Exception as e:
        # В случае ошибки возвращаем 500
        return HttpResponse(f"Ошибка: {str(e)}", status=500)

def home(request):
    problems = Problem.objects.all().order_by('-created_at')
    return render(request, 'trainer/home.html', {
        'problems': problems,
        'now': timezone.now() 
    })

def start_test(request):
    if request.method == 'POST':
        form = TestConfigForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            # Выбор задач в зависимости от темы
            if topic == 'mixed':
                problems = list(Problem.objects.all())
            else:
                problems = list(Problem.objects.filter(topic=topic))
            
            # Проверка наличия задач
            if not problems:
                return HttpResponse("Нет задач для выбранной темы.", status=404)
            
            # Выбираем до 5 случайных задач
            selected_problems = random.sample(problems, min(5, len(problems)))
            
            # Создание сессии с сохранением ID задач
            session = TestSession.objects.create(
                topic=topic,
                user=request.user if request.user.is_authenticated else None,
                problem_ids=[p.id for p in selected_problems]
            )
            return redirect('test-problem', session_id=session.id, problem_num=1)
        else:
            return render(request, 'trainer/test_start.html', {'form': form})
    
    form = TestConfigForm()
    return render(request, 'trainer/test_start.html', {'form': form})

def test_problem(request, session_id, problem_num):
    # Получение сессии
    if request.user.is_authenticated:
        session = get_object_or_404(TestSession, id=session_id, user=request.user)
    else:
        session = get_object_or_404(TestSession, id=session_id, user__isnull=True)
        if str(session.id) != request.COOKIES.get('test_session'):
            raise Http404("Нет доступа к этой сессии теста")
    
    # Получение задач из сохранённых ID
    problem_ids = session.problem_ids
    if not problem_ids or problem_num > len(problem_ids):
        return redirect('test-result', session_id=session.id)
    
    current_problem = Problem.objects.get(id=problem_ids[problem_num - 1])
    
    # Расчёт прогресса
    total_problems = len(problem_ids)
    progress = (problem_num - 1) / total_problems * 100 if total_problems > 0 else 0
    
    if request.method == 'POST':
        user_answer = request.POST.get('answer', '')
        is_correct = check_answer(user_answer, current_problem.answer)
        
        UserAnswer.objects.create(
            session=session,
            problem=current_problem,
            user_answer=user_answer,
            is_correct=is_correct
        )
        
        if is_correct:
            session.score += current_problem.difficulty
            session.save()
        
        if 'finish' in request.POST:
            session.completed = True
            session.save()
            return redirect('test-result', session_id=session.id)
        
        return redirect('test-problem', session_id=session_id, problem_num=problem_num + 1)
    
    return render(request, 'trainer/test_problem.html', {
        'problem': current_problem,
        'problem_num': problem_num,
        'total_problems': total_problems,
        'progress': progress,
        'session': session
    })

def test_result(request, session_id):
    session = get_object_or_404(TestSession, id=session_id)
    answers = UserAnswer.objects.filter(session=session)
    
    # Получаем задачи из сессии по сохранённым ID
    problems = Problem.objects.filter(id__in=session.problem_ids)
    
    # Расчёт максимального балла
    max_score = sum(p.difficulty for p in problems)
    
    # Расчёт оценки
    grade = min(5, (session.score / max_score) * 5) if max_score > 0 else 0
    
    return render(request, 'trainer/test_result.html', {
        'session': session,
        'answers': answers,
        'grade': round(grade, 1),
        'max_score': max_score
    })