from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def view_profile(player_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            resp = await session.get("http://mrush.mobi/view_profile", params={'player_id': player_id})
            await session.close()
            resp_text = await resp.text()
            resp_old = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await view_profile(player_id, cookies, connector)
            clan_name = None
            resp = resp_old.find("div", {"class": "yell mlr10 mt5 mb5"})
            for a in resp.find_all("span", {"class": "nowrap"}):
                if "Клан" in a.text:
                    clan_name = a.find("a").text
            return {'status': 'ok',
                    'clan_name': clan_name}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 59, 'msg': 'view_profile'}
