from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def find_player(name, cookies, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            resp = await session.get("http://mrush.mobi/find_player",
                                     params={"name": name})
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await find_player(name, cookies, connector)
            if "Герой не найден" in await resp.text():
                return {"status": "error",
                        "code": 21,
                        "msg": "Failed to get player"}
            try:
                if "Поиск героя" in await resp.text():
                    resp_text = BeautifulSoup(await resp.read(), "lxml")
                    resp_text = resp_text.find("table",
                                               {"class": "cntr wa mlra"})
                    player_id = resp_text.find("a")["href"].split("=")[1]
                else:
                    player_id = str(resp.url).split("=")[1]
            except:
                player_id = None
            if player_id:
                return {"status": "ok", "player_id": player_id}
            else:
                return {"status": "error",
                        "code": 22,
                        "msg": "Failed to get player"}
    except Exception as e:
        return {"status": "error", "code": 20, "msg": "Failed to get player"}


async def find_clan(name, cookies, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            resp = await session.post("http://mrush.mobi/find_clan",
                                      data={"name": name})
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await find_clan(name, cookies, connector)
            if "Клан не найден" in await resp.text():
                return {"status": "error",
                        "code": 22,
                        "msg": "Failed to get clan"}
            try:
                clan_id = str(resp.url).split("=")[1]
            except:
                clan_id = None
            if clan_id:
                return {"status": "ok", "clan_id": clan_id}
            else:
                return {"status": "error",
                        "code": 23,
                        "msg": "Failed to get clan"}
    except Exception as e:
        return {"status": "error", "code": 24, "msg": "Failed to get clan"}
