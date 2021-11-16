import datetime
import time_machine

from rest_framework          import status
from rest_framework.test     import APITestCase

from research.models         import ResearchInformation


class TestRecentListView(APITestCase):
    maxDiff = None

    def setUp(self):
        self.mocked_date_time1 = datetime.date(2021,11,1)
        self.mocked_date_time2 = datetime.date(2020,1,2)

        with time_machine.travel(self.mocked_date_time1):
            ResearchInformation.objects.create(
            id            = 1,
            name          = '조직구증식증 임상연구',
            number        = 'C140010',
            period        = '3년',
            range         = '국내다기관',
            code          = '관찰연구',
            institute     = '서울아산병원',
            stage         = '코호트',
            target_number = 120,
            office        = 'Pediatrics',
            )

        with time_machine.travel(self.mocked_date_time2):
            ResearchInformation.objects.create(
            id            = 2,
            name          = '조직구증식증 임상연구',
            number        = 'C130010',
            period        = '3년',
            range         = '국내다기관',
            code          = '관찰연구',
            institute     = '서울아산병원',
            stage         = '코호트',
            target_number = 120,
            office        = 'Pediatrics',
            )

    def tearDown(self):
        ResearchInformation.objects.all().delete()

    def test_recent_list_success(self):
        expected_data = [{
            "id"           : 1,
            "name"         : '조직구증식증 임상연구',
            "number"       : 'C140010',
            "period"       : '3년',
            "range"        : '국내다기관',
            "code"         : '관찰연구',
            "institute"    : '서울아산병원',
            "stage"        : '코호트',
            "target_number": 120,
            "office"       : 'Pediatrics',
            "created_at"   : self.mocked_date_time1.strftime('%Y-%m-%d'),
            "updated_at"   : self.mocked_date_time1.strftime('%Y-%m-%d'),
        }]

        with time_machine.travel(self.mocked_date_time1):
            response = self.client.get('/researches/recent')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_data, response.json()['results'])