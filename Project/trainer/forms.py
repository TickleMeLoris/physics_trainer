from django import forms

class TestConfigForm(forms.Form):
    TOPIC_CHOICES = [
        ('kinematics', 'Кинематика'),
        ('dynamics', 'Динамика'),
        ('mixed', 'Смешанный'),
    ]
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, label='Выберите тему')