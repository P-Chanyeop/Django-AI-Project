from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm


# Create your views here.


def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

    """
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    """
    return redirect('pybo:detail', question_id=question.id)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)   # request.POST 인자에는 폼 화면에서 사용자가 입력한 내용들이 담겨져 있다.
        if form.is_valid():     # 폼이 유효하다면.. 이 때 form에는 오류 메시지가 저장되므로 화면에 오류를 표시할 수 있다.
            question = form.save(commit=False)  # 임시 저장(데이터베이스에 저장X) 후 question 객체를 리턴받는다.
            question.create_date = timezone.now()   # 실제 저장을 위해 작성일시 설정
            question.save()     # 데이터를 실제로 저장
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    # {'form': form}은 질문 등록시 사용할 폼 엘리먼트를 생성할 때 사용
    return render(request, 'pybo/question_form.html', context)