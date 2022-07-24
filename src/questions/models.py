from django.db import models
from django.conf import settings


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    asked = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    viewed = models.IntegerField(default=0, editable=False)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question')
    tags = models.ManyToManyField(Tags)
    rating = models.IntegerField(editable=False, default=0)


class Answer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answer')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    rating = models.IntegerField(editable=False, default=0)
    accepted = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class QuestionReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.BooleanField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
