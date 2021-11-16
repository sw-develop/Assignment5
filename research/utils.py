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
    if old_key == '과제명':
        new_key = 'name'
    elif old_key == '과제번호':
        new_key = 'number'
    elif old_key == '연구기간':
        new_key = 'period'
    elif old_key == '연구범위':
        new_key = 'range'
    elif old_key == '연구종류':
        new_key = 'code'
    elif old_key == '연구책임기관':
        new_key = 'institute'
    elif old_key == '임상시험단계(연구모형)':
        new_key = 'stage'
    elif old_key == '전체목표연구대상자수':
        new_key = 'target_number'
    elif old_key == '진료과':
        new_key = 'office'
    else:
        print(old_key)
    return new_key


def convert_dict_to_dataclass(dcls, before, many=False):
    if many:
        return [dcls(**item) for item in before]
    return dcls(**before)
