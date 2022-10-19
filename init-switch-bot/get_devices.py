import json
from pprint import pprint

import requests

from ssm import get_parameters

switch_bot_token = get_parameters(param_key="/switch_bot/token")


def get_device_list():
    res = requests.get(
        'https://api.switch-bot.com/v1.0/devices',
        headers={
            'content-type': 'application/json; charset=utf8',
            'Authorization': switch_bot_token
        }
    )
    return json.loads(res.text)['body']['deviceList']


def main():
    device_list = get_device_list()
    pprint(device_list)


if __name__ == "__main__":
    main()
