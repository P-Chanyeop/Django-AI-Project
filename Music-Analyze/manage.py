#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # 환경변수에 'DJANGO_SETTINGS_MODULE'라는 이름으로 config.settings 라는 문자열을 등록시켜주는 명령어이다.
    # settings.py가 프로젝트 전역에서 사용되기 때문에 이런식으로 환경변수로 넣어 준 것.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # django.core.management 로 부터 execute_from_command_line 이라는 함수를 가져오는 코드로
    # import에 실패하면 장고가 제대로 다운로드 되지 않을 것이므로 ImportError 에러 메세지를 전달하고
    # 아니라면 execute_from_command_line(sys.argv)를 실행 시켜준다.
    # 여기서 sys.argv는 command line(terminal)에서 파이썬 스크립트를 실행시킬 때 python 뒤에 오는 모든 문자열이다.
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    # manage.py는 settings,py의 위치를 환경변수로 등록시켜주고
    # 뒤에 오는 arguments들을 이용 execute_from_command_line을
    # 실행 시켜주는 것을 알 수 있다.


if __name__ == '__main__':
    main()
