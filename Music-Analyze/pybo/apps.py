
# 앱 설정 파일이다. 앱에 대한 설정을 수정할 때 사용한다.
# 장고 프로젝트 이름/settings.py로 이동하여 INSTALLED_APPS에 생성한 앱 이름을 추가합니다.
# 앱이 추가될 때마다 INSTALLED_APPS에 앱 이름을 등록해야 합니다.
# 설치된 앱은 apps.py의 경로 설정을 따라갑니다.

from django.apps import AppConfig


class PyboConfig(AppConfig):
    # 장고가 제공하는 모델 필드 옵션과 필드 유형중 자신이 사용하고자 하는 옵션을 명시.
    # AutoField 옵션은 ID로 사용가능한 자동으로 증가하는 Integer필드 이다.
    # 보통 직접 사용할 필요는 업으며 모델의 기본키 필드는 별도로 지정하지 않으면 자동으로 추가된다.
    # BigAutoField는 AutoField와 매우 유사한 64bit 정수이다. 다만 범위가 매우 넓다. (1 ~ 9223372036854775807, 약 922경의 범위를 가짐)
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'
