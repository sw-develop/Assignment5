from typing import List


def convert_research_data_to_model_form(data_list: List[dict]) -> List[dict]:
    for i in range(len(data_list)):
        temp = {}
        for key, value in data_list[i].items():
            k = _change_key(key)
            v = value
            if k == 'target_number':
                try:
                    v = int(v)
                except ValueError:
                    v = 0
            temp[k] = v
        data_list[i] = temp
    return data_list


def _change_key(old_key):
    keys = {
        "과제명": "name",
        "과제번호": "number",
        "연구기간": "period",
        "연구범위": "range",
        "연구종류": "code",
        "연구책임기관": "institute",
        "임상시험단계(연구모형)": "stage",
        "전체목표연구대상자수": "target_number",
        "진료과": "office"
    }
    return keys[old_key]


def convert_dict_to_dataclass(dcls, before, many=False):
    if many:
        return [dcls(**item) for item in before]
    return dcls(**before)
