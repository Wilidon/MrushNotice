from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Мафия', callback_data='mafiya'),
        ]
    ]
)

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Мафия', callback_data='mafiya'),
        ],
        [
            InlineKeyboardButton(text='Админка',
                                 callback_data='admin'),
            InlineKeyboardButton(text='Статистика',
                                 callback_data='stats')
        ]
    ]
)


notice_off = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да',
                                 callback_data='notice_maf_1'),
            InlineKeyboardButton(text='☑️ Нет',
                                 callback_data='notice_maf_0')
        ],
        [
            InlineKeyboardButton(text='🔽 Назад', callback_data='menu')
        ]
    ]
)

notice_on = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='☑️ Да', callback_data='notice_maf_1'),
            InlineKeyboardButton(text='Нет', callback_data='notice_maf_0')
        ],
        [
            InlineKeyboardButton(text='🔽 Назад', callback_data='menu')
        ]
    ]
)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='В разработке',
                                 callback_data='pass'),
        ],
        [
            InlineKeyboardButton(text='🔽 Назад', callback_data='menu')
        ]
    ]
)

view_users = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Посмотреть пользователей',
                                 callback_data='view_users'),
        ]
    ]
)


stats = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🔽 Назад',
                                 callback_data='menu'),
        ]
    ]
)