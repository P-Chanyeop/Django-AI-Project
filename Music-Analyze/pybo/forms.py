from django import forms
from pybo.models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    # ModelForm은 모델과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할수 있는 폼
    # ModelForm에는 이너클래스인 Meta클래스를 반드시 필요로 함.
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        # create_date 속성은 데이터 저장 시점에 생성해야 하는 값이므로 QuestionForm에 등록하여 사용하지 않는다.

        # 아래의 방법으로 subject, content 입력 필드에 부트스트랩 클래스를 추가할 수 있다.
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }

        label = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }