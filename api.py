import os
import json

import requests

URL = os.getenv('URL')
BK_APP_CODE = os.getenv('BK_APP_CODE')
BK_APP_SECRET = os.getenv('BK_APP_SECRET')


def get_answer(**params):
    headers = {
        'Content-Type': 'application/json',
        'x-bkapi-authorization': {
            'bk_app_code': BK_APP_CODE,
            'bk_app_secret': BK_APP_SECRET
        }
    }
    response = requests.get(URL, headers=headers, params=params)
    try:
        payload = response.json()
        return payload.get('result')
    except json.JSONDecodeError:
        return None
