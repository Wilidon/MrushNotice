from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def clan_members(clan_id, page, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            resp = await session.get("http://mrush.mobi/clan", params={'id': clan_id, 'online': 0, 'page': page})
            await session.close()
            resp = BeautifulSoup(await resp.read(), "lxml")
            players = resp.find_all("a", {'class': 'clan_member'})
            nicks = []
            for player in players:
                nicks.append([player['href'], player.text])
            if nicks:
                return {'status': 'ok', 'threads': nicks}
            else:
                return {'status': 'error', 'code': 15, 'msg': 'Failed to get threads id'}
    except Exception as e:
        return {'status': 'error', 'code': 15, 'msg': 'Failed to get threads id'}