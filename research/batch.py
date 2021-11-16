import datetime
from dataclasses import dataclass
from typing import Set, Tuple

import requests
from django.db import transaction

from research.models import ResearchInformation
from research.serializers import DataResearchSerializer
from research.utils import *


#  값객체: __eq__ 연산을 수행하기 위한 dataclass.
@dataclass(frozen=True)
class DataResearch:
    name: str
    number: str
    period: str
    range: str
    code: str
    institute: str
    stage: str
    target_number: int
    office: str


def get_data_from_open_api():
    # todo:url에 perPage 값
    url = f"https://api.odcloud.kr/api/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887?perPage=100000"
    auth_key = "T6s//nbyXCowhkCB2p7gIX/+eSGn1PT6DppCYV9Ulvg0+cdykw2JQ5w/iwadFVWyE+CgjXZjSHi/auU1E+hG3w=="
    headers = {
        "Authorization": f"Infuser {auth_key}"
    }
    response = requests.get(url, headers=headers)
    data_list = convert_research_data_to_model_form(response.json()['data'])
    set_data_researches = set(convert_dict_to_dataclass(DataResearch, data_list, many=True))
    return set_data_researches


def get_data_from_db():
    ri = ResearchInformation.objects.all()
    ri = DataResearchSerializer(ri, many=True).data
    set_from_db = set(convert_dict_to_dataclass(DataResearch, ri, many=True))
    return set_from_db


def divide_target(set_from_open, set_from_db, for_delete=False) \
        -> Tuple[List[ResearchInformation], List[ResearchInformation]]:
    target: List[DataResearch] = list(set_from_open - set_from_db)
    numbers = [i.number for i in target]
    if for_delete:
        target: List[DataResearch] = list(set_from_db - set_from_open)
        numbers_from_open = [i.number for i in list(set_from_open)]
        numbers = [i.number for i in target if i.number not in numbers_from_open]

    querysets = ResearchInformation.objects.filter(number__in=numbers).values('id', 'number')
    research_for_update_or_delete = []
    research_for_insert = []
    for i in target:
        flag = False
        for j in querysets:
            if i.number == j['number']:
                temp = ResearchInformation(**i.__dict__)
                temp.id = j['id']
                temp.updated_at = datetime.datetime.now()
                research_for_update_or_delete.append(temp)
                flag = True
                break
        if not flag:
            temp = ResearchInformation(**i.__dict__)
            research_for_insert.append(temp)
    return research_for_insert, research_for_update_or_delete


@transaction.atomic()
def batch_task():
    update_fields = [
        'name', 'period', 'range', 'code',
        'institute', 'stage', 'target_number', 'office', 'updated_at'
    ]

    set_from_open: Set[DataResearch] = get_data_from_open_api()
    set_from_db: Set[DataResearch] = get_data_from_db()

    research_for_insert, research_for_update = divide_target(set_from_open, set_from_db)
    _, research_for_delete = divide_target(set_from_open, set_from_db, for_delete=True)

    ResearchInformation.objects.bulk_create(research_for_insert)
    ResearchInformation.objects.bulk_update(research_for_update, update_fields)
    ids_for_delete = [i.id for i in research_for_delete]
    ResearchInformation.objects.filter(id__in=ids_for_delete).delete()
