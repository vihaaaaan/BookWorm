# Generated by Django 5.0.2 on 2024-02-18 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherWorm', '0003_remove_article_original_text_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='difficulty_level_easy_text',
        ),
        migrations.RemoveField(
            model_name='article',
            name='difficulty_level_hard_text',
        ),
        migrations.RemoveField(
            model_name='article',
            name='difficulty_level_medium_text',
        ),
        migrations.AddField(
            model_name='article',
            name='difficulty_level',
            field=models.CharField(choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('HARD', 'Hard'), ('ORIGINAL', 'Original')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='new_text',
            field=models.TextField(null=True),
        ),
    ]
