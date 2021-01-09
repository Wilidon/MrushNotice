from aiogram import types

from config import get_settings
from keyboards import buttons
from sql import crud
from mrush_tg import dp


settings = get_settings()


@dp.callback_query_handler(text="menu")
async def callback_button(call: types.CallbackQuery):
    await call.answer()
    try:
        if call.from_user.id in settings.admins:
            await call.message.edit_text(text="Главное меню",
                                         reply_markup=buttons.admin_menu)
        else:
            await call.message.edit_text(text="Главное меню",
                                         reply_markup=buttons.menu)
    except:
        pass


@dp.callback_query_handler(text="mafiya")
async def callback_button(call: types.CallbackQuery):
    await call.answer()
    user = crud.get_user(user_id=call.from_user.id)
    try:
        if user.notice is False:
            await call.message.edit_text(text="Уведомлять о новых партиях?",
                                         reply_markup=buttons.notice_off)
        else:
            await call.message.edit_text(text="Уведомлять о новых партиях?",
                                         reply_markup=buttons.notice_on)
    except:
        pass


@dp.callback_query_handler(text_contains="notice_maf_")
async def callback_button(call: types.CallbackQuery):
    await call.answer()
    user = crud.update_notice(user_id=call.from_user.id,
                              choice=call.data.split("_")[2])
    try:
        if user.notice is False:
            await call.message.edit_text(text="Уведомлять о новых партиях?",
                                         reply_markup=buttons.notice_off)
        else:
            await call.message.edit_text(text="Уведомлять о новых партиях?",
                                         reply_markup=buttons.notice_on)
    except:
        pass


@dp.callback_query_handler(text="admin")
async def callback_button(call: types.CallbackQuery):
    await call.answer()
    users = crud.get_amount_users()
    text = f"""Админ-панель.\n
Version: 0.9.1\n
Пользователей: {users}"""
    await call.message.edit_text(text=text,
                                 reply_markup=buttons.admin_panel)


@dp.callback_query_handler(text="stats")
async def callback_button(call: types.CallbackQuery):
    await call.answer()
    text = f"""<b>Статистика???</b>\n
А какая собственно статистика нужна в боте, которым пользуется полтора человека??"""
    await call.message.edit_text(text=text,
                                 reply_markup=buttons.stats)


@dp.callback_query_handler(text="pass")
async def callback_button(call: types.CallbackQuery):
    await call.answer()
