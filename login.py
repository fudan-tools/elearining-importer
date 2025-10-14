import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from public import login;
import requests;
def get_cookies():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }

    params = {
        'ticket': login.get_ticket("https://elearning.fudan.edu.cn/login/cas/6"),
    }

    res = requests.get('https://elearning.fudan.edu.cn/login/cas/6', params=params, headers=headers)
    cookies = dict(res.cookies)
    params = {
        'login_success': '1',
    }
    res = requests.get('https://elearning.fudan.edu.cn/dash', params=params, cookies=cookies)
    return dict(res.cookies)