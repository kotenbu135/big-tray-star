import requests

from ssm import get_parameters

webhook_url = get_parameters(param_key="/discord/webhook/spotify_new_release")


def post_discord(content_str):
    header = {'Content-Type': 'application/json'}
    content = {"content": content_str}
    response = requests.post(webhook_url, headers=header, json=content)
    print(response.text)
