from aiogram import types

from config import get_settings
from keyboards import buttons
from scripts.core import get_stats, find_word, block, players, clans
from sql import crud
from mrush_tg import dp

settings = get_settings()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = crud.get_user(user_id=message.from_user.id)
    if user is None:
        crud.add_user(user_id=message.from_user.id,
                      username=message.from_user.username,
                      first_name=message.from_user.first_name,
                      last_name=message.from_user.last_name)
    if message.from_user.id in settings.admins:
        await message.answer("Главное меню", reply_markup=buttons.admin_menu)
    else:
        await message.answer("Главное меню", reply_markup=buttons.menu)


@dp.message_handler(commands=['stats'])
async def send_stats(message: types.Message):
    try:
        if message.from_user.id in settings.admins:
            thread_id = message.text.split(" ")[1]
            if thread_id.isdigit():
                stats, stats2, stats3 = await get_stats(thread_id)
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
                await message.answer(
                    "ID — уникальный признак объекта и должен состоять из "
                    "цифр.")
    except Exception:
        await message.answer("ID не указан.")


@dp.message_handler(commands=['find'])
async def send_stats(message: types.Message):
    await find_word(message)


@dp.message_handler(commands=['block'])
async def send_stats(message: types.Message):
    await block(message)


@dp.message_handler(commands=['players'])
async def send_stats(message: types.Message):
    await players(message)


@dp.message_handler(commands=['clans'])
async def send_stats(message: types.Message):
    await clans(message)


@dp.message_handler(content_types=["text"])
async def echo(message: types.Message):
    await message.answer("test")
    pass
