import datetime
import requests

from dataclasses import dataclass
from typing import Set, Tuple
from django.db import transaction

from humanscape.settings.base import get_env_variable
from research.models import ResearchInformation
from research.serializers import DataResearchSerializer
from research.utils import *


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


def get_data_from_open_api(page_size=10) -> Set[DataResearch]:
    url = f"https://api.odcloud.kr/api/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887?perPage={page_size}"
    # open_api_key = get_env_variable('OPEN_API_KEY')
    open_api_key = "T6s//nbyXCowhkCB2p7gIX/+eSGn1PT6DppCYV9Ulvg0+cdykw2JQ5w/iwadFVWyE+CgjXZjSHi/auU1E+hG3w=="
    headers = {
        "Authorization": f"Infuser {open_api_key}"
    }
    response = requests.get(url, headers=headers)
    data_list = convert_research_data_to_model_form(response.json()['data'])
    set_from_open_api = set(convert_dict_to_dataclass(DataResearch, data_list, many=True))
    return set_from_open_api


def get_data_from_db() -> Set[DataResearch]:
    researches = ResearchInformation.objects.all()
    researches = DataResearchSerializer(researches, many=True).data
    set_from_db = set(convert_dict_to_dataclass(DataResearch, researches, many=True))
    return set_from_db


def divide_target(
        set_from_open_api,
        set_from_db,
        for_delete=False
) -> Tuple[List[ResearchInformation], List[ResearchInformation]]:
    """
    [return value]
    - default: researches_for_insert, researches_for_update
    - for_delete=True: _, researches_for_delete
        - _: Do Not Use
    """
    if for_delete:
        target: List[DataResearch] = list(set_from_db - set_from_open_api)
        numbers_from_open_api = [i.number for i in list(set_from_open_api)]
        numbers = [i.number for i in target if i.number not in numbers_from_open_api]
    else:
        target: List[DataResearch] = list(set_from_open_api - set_from_db)
        numbers = [i.number for i in target]

    querysets = ResearchInformation.objects.filter(number__in=numbers).values('id', 'number')
    researches_for_update_or_delete = []
    researches_for_insert = []

    for i in target:
        flag = False
        for j in querysets:
            if i.number == j['number']:
                temp = ResearchInformation(**i.__dict__)
                temp.id = j['id']
                temp.updated_at = datetime.datetime.now()
                researches_for_update_or_delete.append(temp)
                flag = True
                break
        if not flag:
            temp = ResearchInformation(**i.__dict__)
            researches_for_insert.append(temp)

    return researches_for_insert, researches_for_update_or_delete


@transaction.atomic()
def batch_task():
    update_fields = [
        'name', 'period', 'range', 'code',
        'institute', 'stage', 'target_number', 'office', 'updated_at'
    ]

    set_from_open = get_data_from_open_api(page_size=100000)
    set_from_db = get_data_from_db()

    researches_for_insert, researches_for_update = divide_target(set_from_open, set_from_db)
    _, researches_for_delete = divide_target(set_from_open, set_from_db, for_delete=True)

    ResearchInformation.objects.bulk_create(researches_for_insert)
    ResearchInformation.objects.bulk_update(researches_for_update, update_fields)

    ids_for_delete = [i.id for i in researches_for_delete]
    ResearchInformation.objects.filter(id__in=ids_for_delete).delete()

    return
