"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

# WSGI(Web Server Gateway Interface) 서버 진입점

# WSGI 서버는 웹서버가 동적 페이지 요청을 처리하기 위해 호출하는 서버이다.
# WSGI 서버에는 여러 종류가 있지만 Gunicorn 또는 uwsgi를 가장 많이 사용한다.

# WSGI 서버는 웹 서버와 WSGI 애플리케이션 중간에 위치한다.
# 그래서 WSGI 서버는 WSGI 미들웨어(middleware) 또는 WSGI 컨테이너(container)라고도 한다.
import os

# get_wsgi_application 의 application application이 바로 장고의 애플리케이션이다.
# 이 파일은 장고 프로젝트 생성시 자동으로 만들어지며 특별한 경우가 아니고는 수정할 필요가 없다.
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
