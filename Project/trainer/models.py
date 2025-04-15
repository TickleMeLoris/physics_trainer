from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Problem(models.Model):
    TOPIC_CHOICES = [
        ('kinematics', 'Кинематика'),
        ('dynamics', 'Динамика'),
    ]
    
    topic = models.CharField(
        max_length=20,
        choices=TOPIC_CHOICES,
        verbose_name='Раздел'
    )
    
    description = models.TextField()
    formula = models.CharField(max_length=200)
    answer = models.CharField(max_length=100)
    difficulty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Задача #{self.id}: {self.get_topic_display()}"
    
    def get_previous(self):
        return Problem.objects.filter(id__lt=self.id).order_by('-id').first()
    
    def get_next(self):
        return Problem.objects.filter(id__gt=self.id).order_by('id').first()
    
class TestSession(models.Model):
    TOPIC_CHOICES = [
        ('kinematics', 'Кинематика'),
        ('dynamics', 'Динамика'),
        ('mixed', 'Смешанный'),
    ]
    
    topic = models.CharField(
        max_length=50,
        choices=TOPIC_CHOICES,
        verbose_name='Тема'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    problem_ids = models.JSONField(default=list)
    
    def __str__(self):
        return f"TestSession {self.id} - {self.get_topic_display()}"

class UserAnswer(models.Model):
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField()
