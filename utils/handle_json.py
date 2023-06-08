import json

import yaml

from utils.logger import log as logger


def get_json(path, field=''):
    with open(path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        if field:
            data = json_data.get(field)
            return data
        else:
            return json_data


def write_data(res, json_path, formatter="json"):
    if formatter == "json":
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, sort_keys=True, indent=4)
        logger.info('Всего параметров интерфейса: {}, успешно записано в файл JSON!'.format(len(res)))
    elif formatter in ["yaml", "yml"]:
        with open(json_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(res, stream=f, allow_unicode=True, default_flow_style=False)
        logger.info('Всего параметров интерфейса: {}, успешно записано в файл YAML'.format(len(res)))


def json_to_yaml(json_file):
    if json_file.endswith(".json"):
        with open(json_file, "r") as pf:
            json_to_dict = json.loads(pf.read())
        yaml_file = json_file.replace(".json", ".yaml")
        with open(yaml_file, "w") as fp:
            yaml.safe_dump(json_to_dict, stream=fp, default_flow_style=False)
            logger.info("json to yaml success")
    else:
        logger.info("Неверный формат файла")


def yaml_to_json(yaml_file):
    if yaml_file.endswith(".yml"):
        with open(yaml_file, "r", encoding="utf8") as pf:
            yaml_to_dict = yaml.load(pf, Loader=yaml.FullLoader)
            dict_to_json = json.dumps(yaml_to_dict, sort_keys=False, indent=4, separators=(',', ': '))
        json_file = yaml_file.replace(".yaml", ".json")
        with open(json_file, "w") as fp:
            fp.write(dict_to_json)
            logger.info("yaml to json success")
    else:
        logger.info("Неверный формат файла")
