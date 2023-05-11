import os
import json

import requests

URL = os.getenv('URL')
MODEL_MAP = {
    'chat': 'get_gpt_answer',
    'ko2cn': 'gpt_cn2ko'
}
BK_APP_CODE = os.getenv('BK_APP_CODE')
BK_APP_SECRET = os.getenv('BK_APP_SECRET')


def get_answer(**params):
    """
    input_text,
    session_id,
    model_config
    """
    headers = {
        'Content-Type': 'application/json',
        'x-bkapi-authorization': json.dumps({
            'bk_app_code': BK_APP_CODE,
            'bk_app_secret': BK_APP_SECRET
        })
    }
    try:
        url = f"{URL}{MODEL_MAP[params['model_config']['model']]}/"
    except KeyError:
        return 'Parse error'
    response = requests.post(url, headers=headers, json=params)
    try:
        payload = response.json()
        return payload['data']
    except (json.JSONDecodeError, KeyError):
        return None
