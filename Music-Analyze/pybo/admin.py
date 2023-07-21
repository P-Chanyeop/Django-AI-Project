# admin.py - 해당 앱에 대한 관리자 인터페이스를 등록한다.
# 관리자 페이지에서 우리가 만든 장고(django) 어플리케이션의 모델(Models)을 관리하기 위해서는
# 장고(django) 어플리케이션의 모델(Models)을 등록할 필요가 있다.
# 우리가 사용할 Question, Answer 모델을 여기다 등록한다.
from django.contrib import admin
from .models import Question


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
