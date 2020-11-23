import asyncio

import requests
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def start(name, password, connector):
    pass


async def login(name, password, connector):
    try:
        s = requests.Session()
        r = s.get("https://mrush.mobi/welcome")
        if "я не робот" in r.text:
            resp = BeautifulSoup(r.content, "lxml")
            resp_style = resp.find_all("style")
            for i in resp_style:
                if "margin-left:" in str(i) or "overflow: hidden" in str(i) or \
                        "display: none;" in str(i):
                    pass
                else:
                    code = str(i).split(".")[1].split("{")[0]
                    r = resp.find("div", {"class": code}).find("input")['name']
                    data = {'name': name, 'password': password, r: ''}
                    resp = s.post("https://mrush.mobi/login", data=data)
                    if "Неправильное Имя или Пароль" in resp.text:
                        return {"status": "error",
                                "code": 0,
                                "msg": "Incorrect name or password"}
                    elif "Ваш питомец заблокирован" in resp.text:
                        return {"status": "error",
                                "code": 0,
                                "msg": "This account has blocked"}
                    elif "Магазин" in resp.text:
                        cookies = s.cookies.get_dict()
                        return {"status": "ok",
                                "cookies": cookies}
                    else:
                        return {"status": "asd"}
        else:
            data = {'name': name, 'password': password}
            s.post("https://mrush.mobi/login", data=data)
            cookies = s.cookies.get_dict()
            return {"status": "ok",
                    "cookies": cookies}
    except Exception as e:
        return {'status': 'error',
                'code': 3,
                'msg': 'Authorization failed'}
