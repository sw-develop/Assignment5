from rest_framework         import status
from rest_framework.test    import APITestCase

from research.models        import ResearchInformation

from django.core import serializers


class ResearchRetrieveTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        ResearchInformation.objects.create(
            name="조직구증식증 임상연구 네트워크 구축 및 운영(HLH)",
            number="C130010",
            period="3년",
            range="국내다기관",
            code="관찰연구",
            institute="서울아산병원",
            stage="코호트",
            target_number="120",
            office="Pediatrics",
            created_at="2021-11-16",
            updated_at="2021-11-16"
        )
        ResearchInformation.objects.create(
            name="대한민국 쇼그렌 증후군 코호트 구축",
            number="C130011",
            period="6년",
            range="국내다기관",
            code="관찰연구",
            institute="가톨릭대 서울성모병원",
            stage="코호트",
            target_number="500",
            office="Rheumatology",
            created_at="2021-11-16",
            updated_at="2021-11-16",
        )
        ResearchInformation.objects.create(
            name="Lymphoma Study for Auto",
            number="C100002",
            period="1년",
            range="단일기관",
            code="국내연구",
            institute="가톨릭대 서울성모병원",
            stage="Case-only",
            target_number="200",
            office="Hematology",
            created_at="2021-11-16",
            updated_at="2021-11-16"
        )

    def test_detail_view_success(self):
        response = self.client.get('/researches/C100002')
        
        expected_data_id = ResearchInformation.objects.get(number='C100002').id

        self.assertEqual(response.json()['id'], expected_data_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_view_fail(self):
        response = self.client.get(
            '/researches/C140111'
            )

        self.assertEqual(response.json(), {"detail" : "Not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)