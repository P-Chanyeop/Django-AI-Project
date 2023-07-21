import json
import random

from django.conf import settings
import os

from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from scipy.io import wavfile
from scipy.signal import find_peaks

from ..models import Question

from io import BytesIO
import librosa
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import librosa.display
import base64


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def test(request):
    return render(request, 'pybo/analyze.html')


def analyze_wav(request):
    # wav 파일 경로 설정
    wav_file_path = os.path.join(settings.STATIC_ROOT, 'canon.wav')

    # wav 파일 분석
    sample_rate, data = wavfile.read(wav_file_path)

    # 데이터 분석 및 그래프 생성
    # 시간에 따른 그래프 생성
    time = np.array(range(len(data))) / sample_rate
    plt.plot(time, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # 그래프를 이미지로 변환후 HTTP 응답 반환
    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    plt.close()

    return response


def post_test(request):
    return render(request, 'pybo/post_analyze.html')


def post_analyze(request):
    if request.method == "POST" and request.FILES['file']:
        upload_file = request.FILES['file']

        # 파일 정보 확인
        print(upload_file.name)  # 파일 이름
        print(upload_file.size)  # 파일 크기

        # WAV 파일 경로 설정
        # wav_file_path = upload_file.path

        # WAV 파일 분석
        sample_rate, data = wavfile.read(upload_file.file)

        # 데이터 분석 및 그래프 생성
        # 여기서는 간단히 데이터의 시간에 따른 그래프를 생성합니다.
        time = np.array(range(len(data))) / sample_rate
        plt.plot(time, data)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')

        # # 그래프를 이미지로 변환하여 HTTP 응답으로 반환
        # response = HttpResponse(content_type='image/png')
        # plt.savefig(response, format='png')
        # plt.close()
        # 그래프를 이미지로 저장하고 파일을 읽어서 인코딩
        img_path = 'static/image.png'  # 저장할 이미지 경로
        plt.savefig(img_path, format='png')
        plt.close()

        with open(img_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            # 인코딩된 이미지를 반환
        return HttpResponse(encoded_image)

    return redirect('post_test/')


def show(request):
    return render(request, 'pybo/multi.html')


def plotly(request):
    return render(request, 'pybo/plotly.html')


def plotly_analyze(request):
    import plotly.graph_objs as go
    import plotly
    import statsmodels.api as sm
    from scipy.signal import find_peaks
    import librosa
    # import scipy.signal as signal
    import numpy as np

    # if request.FILES['file']:
    upload_file = request.FILES['file']

    # 파일 서버 저장
    fs = FileSystemStorage()
    print(str(settings.BASE_DIR)+"/file.wav")
    if os.path.exists(str(settings.BASE_DIR)+"/file.wav"):
        os.remove(str(settings.BASE_DIR)+"/file.wav")
    filename = fs.save("file.wav", upload_file)

    # 파일 경로 설정
    upload_file = os.path.join(settings.BASE_DIR, "file.wav")

    # 파일 정보 확인
    # print(upload_file.name)  # 파일 이름
    # print(upload_file.size)  # 파일 크기

    # WAV 파일 경로 설정
    # wav_file_path = upload_file.path

    data, sample_rate = librosa.load(upload_file, sr=44100, mono=True,duration=22)

    # 계이름별 주파수 만들기
    hertz2keys = {440: 'A_4'}
    keys = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    # 440hz 이상 계산
    octave = 4
    pitch_num = 1

    while True:
        if keys[pitch_num % 12] == 'C':
            octave += 1

        if octave > 8:
            break

        # calculate hz
        hz = round(440 * 2 ** (pitch_num / 12), 2)  # 0을 대입하면 440hz 출력

        hertz2keys[hz] = keys[pitch_num % 12] + f'_{octave}'

        pitch_num += 1

    # 440hz 이하 계산
    octave = 4
    pitch_num = -1

    while True:
        if keys[pitch_num % 12] == 'B':
            octave -= 1

        if octave < 0:
            break
        # calculate hz
        hz = round(440 * 2 ** (pitch_num / 12), 2)  # 0을 대입하면 440hz 출력

        hertz2keys[hz] = keys[pitch_num % 12] + f'_{octave}'

        pitch_num -= 1

    path = upload_file

    # 음원 길이 설정(초)
    # duration = 50

    # 1초 단위로 데이터 슬라이싱
    sec = 1
    trim_sec = int(1 / sec)
    n_rows = data.shape[0] // sample_rate * trim_sec  # 지정한 주기로 슬라이싱
    dataset = data.reshape(n_rows, -1)

    result = []  # detection 결과 수집
    for sample in dataset:
        if sample.mean() == 0:  # 구간 내 소리가 없는 경우 0 입력
            result.append(0)  # No Signal
            continue

        autocorrelation = sm.tsa.acf(sample, nlags=200)
        peaks = find_peaks(autocorrelation)[0]  # peak로 간주되는 지점 탐색

        if peaks.shape[0] == 0:  # peak가 없는 경우 0 입력
            result.append(0)  # No Peak
            continue

        lag = peaks[0]
        pitch = int(sample_rate / lag)  # Transform lag into frequency

        result.append(pitch)

    def herts_to_closed_key(hertz):
        """음원이 계이름과 정확하게 일치하는 hertz를 출력하지 않을 경우 근사하는 주파수의 계이름을 출력"""

        if hertz == 0:  # 소리가 없는 경우 No Signal을 출력
            return 'NS'

        herts_array = np.array(list(hertz2keys.keys()))  # 딕셔너리 key값을 리스트로 변경
        closed_index = np.argmin(abs(herts_array - hertz))  # 확인 대상과 가장 가까운 계이름 hertz 찾기
        key = hertz2keys[herts_array[closed_index]]  # 출력

        return key

    print(f"Length: {len(result)}")
    print(result)
    print([herts_to_closed_key(x) for x in result])

    # sample_rate, data = wavfile.read(upload_file.file)
    data, sample_rate = librosa.core.load(upload_file,duration=120,sr=44100,mono=True)
    # 시간에 따른 그래프 데이터 생성
    time = [(i / sample_rate)*44100 for i in range(len(data) // 2)]

    # 소리 분석 데이터 그래프 생성
    data_trace = go.Scatter(x=time, y=data, mode='lines', name='Sound Analysis')

    # 레이아웃 설정
    layout = go.Layout(title='Sound Analysis', xaxis=dict(title='Time (s)'), yaxis=dict(title='Amplitude'))

    # 그래프 객체 생성
    figure = go.Figure(data=[data_trace], layout=layout)

    plot_div = plotly.offline.plot(figure, output_type='div')

    # HTML 코드를 HttpResponse 객체로 반환
    # response = HttpResponse(plot_div)
    data = data.tolist()
    data = json.dumps(data)
    response = {
        'data': result,
        'time': [herts_to_closed_key(x) for x in result]
    }
    return JsonResponse(response)
    # return redirect("show")

    # fig.show()

    # # 그래프를 이미지로 변환후 HTTP 응답 반환
    # response = HttpResponse(content_type='image/png')
    # plt.savefig(response, format='png')
    # plt.close()

    # data = [
    #     go.Bar(
    #         x=['x1', 'x2', 'x3', 'x4'],
    #         y=[11, 13, 17, 19]
    #     )
    # ]
    #
    # layout = plotly.graph_objs.Layout(
    #     title='Bar-chart'
    # )
    #
    # figure = plotly.graph_objs.Figure(
    #     data=data, layout=layout
    # )
    #
    # plot_div = plotly.offline.plot(figure, output_type='div')

    # plots = plotly.offline.plot(
    #     figure, filename='basic_bar_chart.html'
    # )

    # HTML 코드를 HttpResponse 객체로 반환
    # response = HttpResponse(plot_div)
    # return response
