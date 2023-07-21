from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from PIL import Image
import io
from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)   # request.POST 인자에는 폼 화면에서 사용자가 입력한 내용들이 담겨져 있다.
        if form.is_valid():     # 폼이 유효하다면.. 이 때 form에는 오류 메시지가 저장되므로 화면에 오류를 표시할 수 있다.
            question = form.save(commit=False)  # 임시 저장(데이터베이스에 저장X) 후 question 객체를 리턴받는다.
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()   # 실제 저장을 위해 작성일시 설정
            question.save()     # 데이터를 실제로 저장
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    # {'form': form}은 질문 등록시 사용할 폼 엘리먼트를 생성할 때 사용
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


def homepage(request):
    return render(request, 'pybo/index.html')
