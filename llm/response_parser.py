import json


def get_message(response_json):

    return response_json["choices"][0]["message"]["content"]


def get_json(response_json):

    content = get_message(response_json)

    return json.loads(content)