import asyncio
from operator import itemgetter

from config import get_settings
from mrushapi import MrushApi
from sql import crud

settings = get_settings()


async def sort_and_print(nicks, count, mrush):
    try:
        data = []
        stats = "<pre>"
        stats2 = stats3 = False
        for pet_id, nick in nicks.items():
            data.append([pet_id, nick, count[pet_id]])
        data = sorted(data, key=itemgetter(2), reverse=True)
        num = 1
        for i in data:
            prof = await mrush.view_profile(i[0])
            if prof['status'] == 'ok':
                if len(data) == num:
                    stats = stats + "{}. [url=/view_profile?player_id={}]{}[" \
                                    "/url] ({}) — {} сообщений.</pre>".format(
                        num, i[0],
                        i[1], prof['clan_name'], i[2])
                else:
                    stats = stats + "{}. [url=/view_profile?player_id={}]{}[/url] ({}) — {} сообщений; \n".format(
                        num, i[0],
                        i[1], prof['clan_name'], i[2])
            else:
                if len(data) == num:
                    stats = stats + "{}. [url=/view_profile?player_id={}]{}[" \
                                    "/url] — {} сообщений.</pre>".format(
                        num, i[0],
                        i[1], i[2])
                else:
                    stats = stats + "{}. [url=/view_profile?player_id={}]{}[/url] — {} сообщений; \n".format(
                        num, i[0],
                        i[1], i[2])
            if len(stats) > 4000:
                if stats2 and len(stats2) > 4000:
                    stats3 = stats2
                    stats = stats + "</pre>"
                    stats2 = stats
                    stats = "<pre>\n"
                else:
                    stats = stats + "</pre>"
                    stats2 = stats
                    stats = "<pre>\n"
            num += 1
        return stats, stats2, stats3
    except Exception as e:
        return "Ошибка (sort_and_print) {}".format(e)


async def get_stats(thread_id):
    try:
        mrush = MrushApi(settings.name, settings.password)
        await mrush.login()
        page, nicks, count, nicks_page, count_page = 1, {}, {}, {}, {}
        while True:
            r = await mrush.thread(thread_id, page)
            if r['status'] == 'error' and r['code'] == 1:
                break
            for i in r['messages']:
                nicks[i['pet_id']] = i['name']
                nicks_page[i['pet_id']] = i['name']
                try:
                    count[i['pet_id']] += 1
                except:
                    count[i['pet_id']] = 1
                try:
                    count_page[i['pet_id']] += 1
                except:
                    count_page[i['pet_id']] = 1
            nicks_page = {}
            count_page = {}
            page += 1
        stats = await sort_and_print(nicks, count, mrush)
        return stats
    except Exception as e:
        return "Ошибка (get_stats) {}".format(e)


async   def sort_word(total_word):
    try:
        stats = "<pre>"
        stats2 = stats3 = False
        num, count = 1, 1
        for key, value in total_word.items():
            for i in value:
                if len(total_word) == count:
                    stats = stats + "{}. [url=/view_profile?player_id={}]{}[/url] — {} страница.</pre>".format(
                        num, i[0],
                        i[1], key)
                else:
                    stats = stats + "{}. [url=/view_profile?player_id={}]{}[/url] — {} страница; \n".format(
                        num, i[0],
                        i[1], key)
                if len(stats) > 4000:
                    if stats2 and len(stats2) > 4000:
                        stats3 = stats2
                        stats = stats + "</pre>"
                        stats2 = stats
                        stats = "<pre>"
                    else:
                        stats = stats + "</pre>"
                        stats2 = stats
                        stats = "<pre>"
                num += 1
            count += 1
        return stats, stats2, stats3
    except Exception as e:
        return "Ошибка (sort_word) {}".format(e)


async def find_word(message):
    try:
        user_id = message.from_user.id
        if user_id in settings.admins:
            thread_id = message.text.split(" ")[1]
            word = message.text.split(" ")[2]
            mrush = MrushApi(settings.name, settings.password)
            r = await mrush.login()
            page, nicks, count, nicks_page, count_page = 1, {}, {}, {}, {}
            total_word = {}
            while True:
                r = await mrush.thread(thread_id, page)
                if r['status'] == 'error' and r['code'] == 0:
                    await message.answer("Возникла непредвиденная ошибка. Попробуйте еще раз!")
                    return 0
                if r['status'] == 'error' and r['code'] == 1:
                    break
                if r['status'] == 'error' and r['code'] == 2:
                    await message.answer("Топ не найден.")
                    return 0
                for i in r['messages']:
                    if word.lower() in i['message'].lower():
                        if page in total_word:
                            for j in range(len(total_word[page])):
                                if i['pet_id'] in total_word[page][j]:
                                    total_word[page][j][2] += 1
                                    break
                            else:
                                total_word[page].append(
                                    [i['pet_id'], i['name'], 1])
                        else:
                            total_word[page] = []
                            total_word[page].append(
                                [i['pet_id'], i['name'], 1])
                page += 1
            stats, stats2, stats3 = await sort_word(total_word)
            if stats3:
                await message.answer(stats3)
                await message.answer(stats2)
                await message.answer(stats)
            elif stats2:
                await message.answer(stats2)
                await message.answer(stats)
            else:
                await message.answer(stats)
        else:
            pass
    except:
        raise
        pass


async def check_word_in_thread(account, thread_id):
    try:
        data = await account.thread(thread_id)
        if "заявок" in data['messages'][0]['message'] \
                and "мест" in data['messages'][0]['message'] \
                and "Мафия" in data['thread_name']:
            return True
        return False
    except:
        raise
        return False


async def mrush_notice(bot):
    forums_id = [35367, 117911]
    account = MrushApi(settings.name, settings.password)
    await account.login()
    while True:
        for forum_id in forums_id:
            await asyncio.sleep(1)
            try:
                threads = await account.threads(forum_id)
                await asyncio.sleep(1)
                for thread_id in threads['threads']:
                    if await check_word_in_thread(account, thread_id) \
                            and crud.get_thread(thread_id) is None:
                        users = crud.notice()
                        for user in users:
                            try:
                                await bot.send_message(user.user_id,
                                                       "Идет набор на новую "
                                                       "партию [мафии]("
                                                       "http://mrush.mobi/thread?id={})\.".format(
                                                           thread_id),
                                                       parse_mode='MarkdownV2')
                            except Exception as e:
                                pass
                        crud.add_thread(thread_id)
            except Exception:
                pass


async def block(message):
    try:
        user_id = message.from_user.id
        if user_id in settings.admins:
            blocked_id = message.text.split(" ")[1]
            user = crud.block(blocked_id)
            if user:
                await message.answer(f"Пользователеь {user.first_name} "
                                     f"заблокирован.")
            else:
                await message.asnwer("Пользователя несуществует.")
    except:
        pass


async def players(message):
    user_id = message.from_user.id
    if not(user_id in settings.admins):
        return 0
    try:
        try:
            names = message.text.split(" ", maxsplit=1)[1].split(", ")
        except:
            await message.answer("Не удалось найти ники.")
            return 0
        account = MrushApi(settings.name, settings.password)
        await account.login()
        text = ""
        for name in names:
            profile = await account.find_player(name)
            if profile["status"] == 'ok':
                text += f"[url=view_profile?player_id=" \
                        f"{profile['player_id']}]{name}[/url]\n"
        if text:
            await message.answer(text)
    except:
        pass


async def clans(message):
    user_id = message.from_user.id
    if not(user_id in settings.admins):
        return 0
    try:
        try:
            names = message.text.split(" ", maxsplit=1)[1].split(", ")
        except:
            await message.answer("Не удалось найти кланы.")
            return 0
        account = MrushApi(settings.name, settings.password)
        await account.login()
        text = ""
        for name in names:
            clan = await account.find_clan(name)
            if clan["status"] == 'ok':
                text += f"[url=clan?id=" \
                        f"{clan['clan_id']}]{name}[/url]\n"
        await message.answer(text)
    except:
        pass
