"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# urls.py 파일은 페이지 요청이 발생하면 가장 먼저 호출되는 파일로 URL과 뷰 함수 간의 매핑을 정의한다.
# 뷰 함수는 views.py 파일에 정의된 함수를 말한다.
from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),  # '/'에 해당하는 path

    # test.py
    path('test/', base_views.test, name='test'),
    path('analyze/', base_views.analyze_wav, name='analyze_wav'),
    path('show/', base_views.show, name='show'),

    # matplotlib.py
    path('post_test/', base_views.post_test, name='post_test'),
    path('post_analyze/', base_views.post_analyze, name='post_analyze'),

    # plotly.py
    path('plotly/', base_views.plotly, name='plotly'),
    path('plotly_analyze/', base_views.plotly_analyze, name='plotly_analyze'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
