# 애플리케이션의 데이터 모델을 정의하는 파일이다.
# 데이터베이스의 필드 및 데이터를 관리함. MVT 패턴 중 모델(Model)을 의미한다.
# 장고 프레임워크에서는 View를 Template, Controller는 View라고 표현하며,
# MVC를 MVT패턴이라고 한다. 모델은 데이터 베이스에 저장되는 데이터를 의미하는 것이고, (Spring Framework의 MVC패턴과 유사)
# 템플릿은 사용자에게 보여지는 UI부분을 담당하고,
# 뷰는 실질적으로 프로그램 로직이 동작하여 데이터를 가져오고 적절하게 처리한 결과를 템플릿에 전달하는 역할을 수행한다.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_question")
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name="voter_question")  # 추천인 추가

    def __str__(self):
        return self.subject
    

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_answer")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name="voter_answer")  # 추천인 추가


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)