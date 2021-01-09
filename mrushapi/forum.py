from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def threads(forum_id, page, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            resp = await session.get("http://mrush.mobi/threads", params={'id': forum_id, 'page': page})
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await threads(forum_id, page, cookies, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            links = []
        for link in resp.find_all("a", href=True):
            a = link["href"]
            links.append(str(a))
        links = [i.split('=')[1] for i in links if 'thread?id' in i]
        links = [i.rsplit("&")[0] for i in links]
        if links:
            return {'status': 'ok', 'threads': links}
        else:
            # TODO
            return {'status': 'error', 'code': 15, 'msg': 'Failed to get threads id'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 15, 'msg': 'Failed to get threads id'}


async def thread(thread_id, page, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id, 'page': page}
            messages = []
            resp = await session.get('https://mrush.mobi/thread', params=params)
            await session.close()
            resp_text = await resp.text()
            resp_old = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread(thread_id, page, cookies, connector)
            elif "Сообщений нет" in resp_text:
                # TODO
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                # TODO
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
            resp = resp_old.find("div", {"class": "wr8"})
            thread_name = resp_old.find("div", {"class": "rr"}).text.replace('\n', '').replace('\t', '')
            for a in range(len(resp.find_all("div", {"class": "ml10 mt2 mb5 mr10 sh wwr"}))):
                pet_id = resp.find_all("a", {"class": "tdn lwhite"})[a]['href'].split("=")[1]
                name = resp.find_all("a", {"class": "tdn lwhite"})[a].text
                message = resp.find_all("div", {"class": "ml10 mt2 mb5 mr10 sh wwr"})[a].text
                post_date = resp.find("span", {"class": "grey1 small"}).text
                message_id = (15 * (int(page) - 1)) + a + 1
                message = dict(pet_id=pet_id, name=name, message_id=message_id, message=message, post_date=post_date)
                messages.append(message)
            return {'status': 'ok',
                    'thread_id': thread_id,
                    'thread_name': thread_name,
                    'page': page,
                    'messages': messages
                    }
    except Exception as e:
        return {'status': 'error',
                'code': 0,
                'msg': e}