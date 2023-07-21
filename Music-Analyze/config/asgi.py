"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
# ASGI(Asynchronous Server Gateway Interface) 서버 진입점
# 기존 WSGI 및 기타 기본적으로 동기 동작을 전제하는 표준은 비동기의 성능이나 효율성이 떨어진다.
# 이는 곧 WSGI가 웹소켓과 같은 고급 프로토콜을 효과적으로 처리하지 못한다는 것을 의미
# web server와 프레임워크(Django), 어플리케이션을 비동기로 연결해 주는 Python의 표준 인터페이스라고 보면 된다.
# 여러 프로토콜 스타일을 처리 할 수 있다(HTTP, HTTP/2, WebSocket 포함)

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
