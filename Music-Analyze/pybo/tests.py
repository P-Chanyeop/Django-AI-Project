from django.test import TestCase

# Create your tests here.
# 웹사이트가 성장함에 따라 손으로 일일히 테스트하는 것은 점점 더 어려워진다. 테스트 할 내용이 늘어날 뿐만 아니라,
# 컴포넌트간의 상호작용도 복잡해지고, 한 쪽의 작은 수정이 다른쪽에 큰 영향을 줄수 있기 때문에, 모든것이 잘 동작할 수 있도록 더 많은 수정이 필요해지며,
# 그렇게 추가된 수정이 새로운 에러를 유발하지 않도록 확인되어야 한다.
# 이러한 문제들의 해결책중 하나는, 쉽고 안정적으로 수정사항이 발생할 때마다 실행되는 자동화된 테스트를 작성하는 것이다
import sys

if __name__ == '__main__':
    print(sys.argv)