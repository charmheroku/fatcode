# Generated by Django 4.0.6 on 2022-07-15 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='CodeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('slug', models.SlugField()),
                ('view_count', models.IntegerField(default=0, editable=False)),
                ('published', models.DateField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_type', models.CharField(choices=[('quiz', 'Квиз'), ('python', 'Python'), ('sql', 'SQL'), ('js', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS')], max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('viewed', models.IntegerField(default=0, editable=False)),
                ('video_url', models.URLField(max_length=500)),
                ('published', models.DateField(auto_now_add=True)),
                ('sorted', models.IntegerField(default=1)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['sorted'],
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('right', models.BooleanField()),
                ('hint', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('code', models.TextField(blank=True, null=True)),
                ('quiz', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserCourseThrough',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='courses.course')),
            ],
        ),
    ]
