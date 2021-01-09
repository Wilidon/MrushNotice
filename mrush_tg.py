import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils import executor

import config
from scripts.core import mrush_notice
from sql import models
from sql.database import engine

settings = config.get_settings()

loop = asyncio.get_event_loop()
bot = Bot(token=settings.token, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop)


if __name__ == '__main__':
    from handlers import dp

    models.Base.metadata.create_all(bind=engine)
    loop.create_task(mrush_notice(bot))
    executor.start_polling(dp, skip_updates=False)
