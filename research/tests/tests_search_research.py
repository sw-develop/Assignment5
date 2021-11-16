from django.db.models       import Q
from rest_framework         import status
from rest_framework.test    import APITestCase

from research.models        import ResearchInformation


class SearchResearchTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        ResearchInformation.objects.create(
            name            =   "조직구증식증 임상연구 네트워크 구축 및 운영(HLH)",
            number          =   "C130010",
            period          =   "3년",
            range           =   "국내다기관",
            code            =   "관찰연구",
            institute       =   "서울아산병원",
            stage           =   "코호트",
            target_number   =   120,
            office          =   "Pediatrics"
        )
        ResearchInformation.objects.create(
            name            =   "대한민국 쇼그렌 증후군 코호트 구축",
            number          =   "C130011",
            period          =   "6년",
            range           =   "국내다기관",
            code            =   "관찰연구",
            institute       =   "가톨릭대 서울성모병원",
            stage           =   "코호트",
            target_number   =   500,
            office          =   "Rheumatology"
        )
        ResearchInformation.objects.create(
            name            =   "Lymphoma Study for Auto-PBSCT",
            number          =   "C100002",
            period          =   "1년",
            range           =   "단일기관",
            code            =   "국내연구",
            institute       =   "가톨릭대 서울성모병원",
            stage           =   "Case-only",
            target_number   =   200,
            office          =   "Hematology"
        )

    def get_filtered_queryset(self, name, range, code, institute, stage, office):
        return ResearchInformation.objects.filter(
            name__icontains         =   name,
            range__icontains        =   range,
            code__icontains         =   code,
            institute__icontains    =   institute,
            stage__icontains        =   stage,
            office__icontains       =   office
        )

    def test_filter_research_information_success(self):
        name      = "국내"
        code      = "관찰연구"
        institute = "병원"
        stage     = "코호트"
        office    = "P"

        response = self.client.get(
            f'/researches?name={name}&range={range}&code={code}&institute={institute}&stage={stage}&office={office}'
        )

        filtered_queryset = self.get_filtered_queryset(name, range, code, institute, stage, office)

        expected_number_of_data = filtered_queryset.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), expected_number_of_data)

    def test_filter_research_information_failed_when_given_query_param_type_is_invalid(self):
        response = self.client.get(
            '/researches?min_target_number=최소값&max_target_number=최대값'
        )

        self.assertEqual(response.data['min_target_number'][0], "Enter a number.")
        self.assertEqual(response.data['max_target_number'][0], "Enter a number.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def get_search_filtered_queryset(self, search):
        return ResearchInformation.objects.filter(
            Q(name__icontains=search) |
            Q(number__icontains=search) |
            Q(range__icontains=search) |
            Q(code__icontains=search) |
            Q(institute__icontains=search) |
            Q(stage__icontains=search) |
            Q(office__icontains=search)
        )

    def test_search_research_information_success(self):
        search = "국내"

        response = self.client.get(
            f'/researches?search={search}'
        )

        filtered_queryset = self.get_search_filtered_queryset(search)

        expected_number_of_data = filtered_queryset.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), expected_number_of_data)
