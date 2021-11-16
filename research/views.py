from datetime                import timedelta, date
from drf_yasg.utils          import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.generics import RetrieveAPIView

from django_filters.rest_framework  import DjangoFilterBackend
from rest_framework.filters         import OrderingFilter, SearchFilter
from rest_framework.generics        import RetrieveAPIView, ListAPIView

from .models       import ResearchInformation
from .filters      import ResearchFilter
from .serializers  import ResearchInformationSerializer

@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id ="연구 데이터 상세 조회",
    operation_description ="연구 번호를 입력하세요\n\n" +
                            "예시 : C160008",
    responses    = {
        "201": "SUCCESS",
        "404": "NOT_FOUND",
        "400": "BAD_REQUEST",
    }
))
class ResearchRetrieveView(RetrieveAPIView):
    queryset            = ResearchInformation.objects.all()
    serializer_class    = ResearchInformationSerializer
    lookup_field        = 'number'


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id ="연구 데이터 검색",
    operation_description = "전체 연구 데이터를 필터 및 검색합니다.\n\n"
                            "필터 : 과제명(name), 연구기간(range), 연구종류(code), 연구책임기관(institute), 임상시험단계(연구모형)(stage), 연구책임기관(institute), 임상시험단계(stage), 전체목표연구대상자수(target_number), 진료과(office), 최고 연구기간(min_target_number), 최대 연구기간(max_target_number)의 필터 및 개별 검색 가능\n\n" +
                            "전체 검색 : search 값에 검색하고 싶은 단어 입력" +
                            "(과제명, 과제번호, 연구기간, 연구종류, 연구책임기관, 임상시험단계(연구모형), 진료과 중 검색 가능)\n\n" +
                            "정렬 : 업데이트된 날짜 역순으로 기본 정렬, 기준으로 정렬하고 싶은 컬럼의 키값을 ordering에 입력하세요\n\n" +
                            "예시 : \n" +
                            "{\n"+
                                "id: 10,\n"+
                                "name: 제2형 당뇨병 임상연구네트워크 구축사업\n"+
                                "number: C140014\n"+
                                "period: 120개월\n"+
                                "range: 국내다기관\n"+
                                "code: 관찰연구\n"+
                                "institute: 경희대학교병원\n"+
                                "stage: 코호트\n"+
                                "target_number: 700\n"+
                                "office: Endocrinology\n"+
                                "created_at: 2021-11-16\n"+
                                "updated_at: 2021-11-16\n"+
                            "}",
    responses    = {
        "201": "SUCCESS",
        "404": "NOT_FOUND",
        "400": "BAD_REQUEST",
    }
))
class SearchResearchView(ListAPIView):
    queryset            = ResearchInformation.objects.all()
    serializer_class    = ResearchInformationSerializer
    filter_backends     = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class     = ResearchFilter
    ordering            = ['-updated_at']
    search_fields       = ['name', 'number', 'range', 'code', 'institute', 'stage', 'office']



@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id ="연구 데이터 전체 리스트 조회",
    operation_description ="최근 7일간 업데이트된 연구 데이터의 전체 리스트를 조회합니다.",
    responses    = {
        "201": "SUCCESS",
        "404": "NOT_FOUND",
        "400": "BAD_REQUEST",
    }
))
class RecentListView(ListAPIView):
    serializer_class = ResearchInformationSerializer
    filter_backends  = [OrderingFilter]
    ordering         = ['-updated_at']

    def get_queryset(self):
        return ResearchInformation.objects.filter(updated_at__range = [date.today() - timedelta(days = 7), date.today()])