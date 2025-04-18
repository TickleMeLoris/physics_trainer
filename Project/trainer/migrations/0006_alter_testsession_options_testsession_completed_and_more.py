# Generated by Django 5.2 on 2025-04-12 13:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0005_remove_testsession_completed_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testsession',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='testsession',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsession',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testsession',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='testsession',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='testsession',
            name='topic',
            field=models.CharField(choices=[('kinematics', 'Только кинематика'), ('dynamics', 'Только динамика'), ('mixed', 'Смешанный тест')], max_length=20),
        ),
    ]
