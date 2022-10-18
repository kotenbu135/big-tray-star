import json

import requests

from ssm import get_parameters

switch_bot_token = get_parameters(param_key="/switch_bot/token")
device_id_bot_1 = get_parameters(param_key="/switch_bot/device_id/bot_1")

# https://github.com/OpenWonderLabs/SwitchBotAPI


def open_intercom():
    body = {
        "commandType": "command",
        "command": "press"
    }
    res = requests.post(
        f'https://api.switch-bot.com/v1.0/devices/{device_id_bot_1}/commands',
        headers={
            'content-type': 'application/json; charset=utf8',
            'Authorization': switch_bot_token
        },
        json=body
    )
    return json.loads(res.content.decode())
