import copy
import json
import jsonpath

from common.get_values import create_base_case

change_json = []


def original_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        info_dict = json.load(f)
    return info_dict


def change_data(real_data, path):
    copy_data = copy.deepcopy(real_data)
    if jsonpath.jsonpath(copy_data, "$..json"):
        modify_data = real_data['request']['json']
        change_list = create_base_case(modify_data)
        num = 0
        for k in real_data['request']['json'].keys():
            for i in change_list:
                save_json = copy_data['request']['json'][k] = i
                change_json.append(save_json)
                if num < len(change_list):
                    print(len(change_list))
                    path_r = path.split('.')[0] + str(num) + '.json'
                    with open(path_r, 'w', encoding='utf-8') as f1:
                        f1.write(json.dumps(copy_data, indent=4, ensure_ascii=False))
                        f1.close()
                        num = num + 1
        change_list.clear()

    elif jsonpath.jsonpath(copy_data, "$..params"):
        modify_data = real_data['request']['params']
        change_list = create_base_case(modify_data)
        num = 0
        for k in real_data['request']['params'].keys():
            for i in change_list:
                save_json = copy_data['request']['params'][k] = i
                change_json.append(save_json)
                if num < len(change_list):
                    print(len(change_list))
                    path_r = path.split('.')[0] + str(num) + '.json'
                    with open(path_r, 'w', encoding='utf-8') as f1:
                        f1.write(json.dumps(copy_data, indent=4, ensure_ascii=False))
                        f1.close()
                        num = num + 1
        change_list.clear()
