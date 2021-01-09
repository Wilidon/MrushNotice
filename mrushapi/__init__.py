import asyncio

from mrushapi import authorization, forum, profile, main


class MrushApi:
    def __init__(self, name=None, password=False, cookies=None, connector=None):
        self.name = name
        self.password = password
        self.connector = connector

    async def start(self, name="standard", password=False):
        """ Регистрация

            Args:
                name (str): Имя аккаунта (default: стандартный);
                password (str): Пароль аккаунта (default: генерируется 10-значный).

            Resp:
                pet_id (int): id аккаунта;
                name (str): Имя аккаунта;
                password (str): Пароль от аккаунта;
                cookies (dict): Куки.
        """
        resp = await authorization.start(name=name, password=password, connector=self.connector)
        if resp['status'] == 'ok':
            self.cookies = resp['cookies']
            self.pet_id = resp['pet_id']
        return resp

    async def login(self):
        """ Авторизация

            Resp:
                cookies (dict): Куки
        """
        resp = await authorization.login(name=self.name, password=self.password,
                                         connector=self.connector)
        if resp['status'] == 'ok':
            self.cookies = resp['cookies']
        return resp

    async def threads(self, forum_id, page=1):
        return await forum.threads(forum_id, page, self.cookies, self.connector)

    async def thread(self, thread_id, page=1):
        return await forum.thread(thread_id, page, self.cookies, self.connector)

    async def view_profile(self, player_id):
        return await profile.view_profile(player_id, self.cookies, self.connector)

    async def find_player(self, name):
        return await main.find_player(name, self.cookies, self.connector)

    async def find_clan(self, name):
        return await main.find_clan(name, self.cookies, self.connector)