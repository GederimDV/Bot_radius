# -*-coding:utf-8-*-
import telebot
import configs
import MySqlUsers
import MySqlGroup
from telebot import types, apihelper

apihelper.proxy = configs.proxy

bot = telebot.TeleBot(configs.token)

print(bot.get_me())


@bot.message_handler(commands=['start'])
def handle_text_start(message):
    print(message.chat.id)
    if configs.i_m == message.chat.id or configs.admin2 == message.chat.id or configs.admin3 == message.chat.id or configs.admin == message.chat.id:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать', 'Информация', 'Редактировать']])
        bot.send_message(message.chat.id, '`Создать` - создать учетную запись пользователя или группу для подключения к сети\n\n'
                                          '`Информация` - получить информацию об устройствах пользователя и его пароля\n\n'
                                          '`Редактировать` - редактировать учетную запись пользователя',
                                          parse_mode="Markdown", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'У вас нет прав, если что-то интересует, напишите сюда @Me5H4X')
        bot.send_message(configs.i_m, "@{u} ломится".format(u=message.chat.username))


@bot.message_handler(commands=['help'])
def handle_text_help(message):
    if configs.i_m == message.chat.id or configs.admin2 == message.chat.id or configs.admin3 == message.chat.id or configs.admin == message.chat.id:
        bot.send_message(message.chat.id, '`Создать` - создать учетную запись пользователя или группу для подключения к сети\n\n'
                                          '`Информация` - получить информацию об устройствах пользователя и его пароля\n\n'
                                          '`Редактировать` - редактировать учетную запись пользователя',
                                          parse_mode="Markdown")


@bot.message_handler(regexp="Создать")
def choose(message):
    if configs.i_m == message.chat.id or configs.admin2 == message.chat.id or configs.admin3 == message.chat.id or configs.admin == message.chat.id:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать пользователя', 'Создать группу']])
        select = bot.send_message(message.chat.id, 'Пользователя или группу?', reply_markup=keyboard)
        bot.register_next_step_handler(select, create_new_user_or_group)


def create_new_user_or_group(message):
    if message.text == 'Создать группу':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['◀️ Назад']])
        name = bot.send_message(message.chat.id, "Напишите название группы",
                                reply_markup=keyboard)
        bot.register_next_step_handler(name, description_group)

    elif message.text == 'Создать пользователя':

        groups = MySqlGroup.groups('')
        groups.append('◀️ Назад')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in groups])
        select = bot.send_message(message.chat.id,
                                  "Выберите группу в которой будет добавлен пользователь",
                                  reply_markup=keyboard)
        bot.register_next_step_handler(select, continue_create_user)


def description_group(message):
    if message.text == '◀️ Назад':
        choose(message)
    else:
        global name_group
        name_group = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['◀️ Назад']])
        description = bot.send_message(message.chat.id, "Напишите описание группы", reply_markup=keyboard)
        bot.register_next_step_handler(description, create_group)


def create_group(message):
    if message.text == '◀️ Назад':
        message.text = 'Создать группу'
        create_new_user_or_group(message)
    else:
        MySqlGroup.create_group(name_group, message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать', 'Информация', 'Редактировать']])
        bot.send_message(message.chat.id, "Группа создана. Дальнейшие действия?", reply_markup=keyboard)


def continue_create_user(message):
    if message.text == '◀️ Назад':
        choose(message)
    else:
        global group_n
        group_n = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['❌ ОТМЕНА ❌']])
        name_user = bot.send_message(message.chat.id, "Напишите ФИО пользователя",
                                     reply_markup=keyboard)
        bot.register_next_step_handler(name_user, write_fio)


def write_fio(message):
    if message.text == '❌ ОТМЕНА ❌':
        handle_text_start(message)
    else:
        global fio_u
        fio_u = message.text
        fio = bot.send_message(message.chat.id, "Напишите email пользователя")
        bot.register_next_step_handler(fio, email_user)


def email_user(message):
    global email
    email = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(command) for command in ['✅', '❌']])
    confirm = bot.send_message(message.chat.id, 'Подтверждаете введенные данные? '
                                                '\nФИО: {f} \nE-mail: {e} \nГруппа: {g}'.
                               format(f=fio_u, e=email, g=group_n), reply_markup=keyboard)
    bot.register_next_step_handler(confirm, create_user)


def create_user(message):
    if message.text == '✅':
        MySqlUsers.create_user(email, fio_u, group_n)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать', 'Информация', 'Редактировать']])
        password = MySqlUsers.UsersPassword(email)
        bot.send_message(message.chat.id, "Пользователь создан. \nЛогин: {e} \nПароль: {p}".format(e=email, p=password),
                         reply_markup=keyboard)
    else:
        groups = MySqlGroup.groups('')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in groups])
        select = bot.send_message(message.chat.id, "Начните с выбора группы", reply_markup=keyboard)
        bot.register_next_step_handler(select, continue_create_user)


@bot.message_handler(regexp="Информация")
def print_groups(message):
    if configs.i_m == message.chat.id or configs.admin2 == message.chat.id or configs.admin3 == message.chat.id or configs.admin == message.chat.id:
        groups = MySqlGroup.groups('')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in groups])
        bot.send_message(message.chat.id, "Выберите группу", reply_markup=keyboard)


@bot.message_handler(regexp="Редактировать")
def select_group(message):
    if configs.i_m == message.chat.id or configs.admin2 == message.chat.id or configs.admin3 == message.chat.id or configs.admin == message.chat.id:
        groups = MySqlGroup.groups('')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in groups])
        select_g = bot.send_message(message.chat.id, "Выберите группу", reply_markup=keyboard)
        bot.register_next_step_handler(select_g, select_user)


def select_user(message):
    users = MySqlGroup.groups(message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(command) for command in users])
    select_u = bot.send_message(message.chat.id, "Выберите пользователя", reply_markup=keyboard)
    bot.register_next_step_handler(select_u, select_edit)


def select_edit(message):
    global edit_user
    edit_user = message.text
    details = MySqlUsers.details_users(message.text)
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(command) for command in ['статус', 'пароль', 'группа', 'ФИО']])
    select = bot.send_message(message.chat.id, "{d}".format(d=details), reply_markup=keyboard)
    bot.register_next_step_handler(select, branch)


def branch(message):
    if message.text == 'статус':
        keyboard = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Cтатус", reply_markup=keyboard)

        status = MySqlUsers.get_status(edit_user)
        if status == '❌':
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(*[types.InlineKeyboardButton(text=s, callback_data=s) for s in '✅'])
        elif status == '✅':
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(*[types.InlineKeyboardButton(text=s, callback_data=s) for s in '❌'])
        bot.send_message(message.chat.id,
                         "Пользователь: {u} \nСтатус: {s}".format(u=edit_user, s=status), reply_markup=keyboard)

    elif message.text == 'пароль':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Сгенерировать', 'Отмена']])
        pswd = bot.send_message(message.chat.id, "Сгенерировать новый пароль?", reply_markup=keyboard)
        bot.register_next_step_handler(pswd, branch2)

    elif message.text == 'группа':
        groups = MySqlGroup.groups('')
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in groups])
        g = bot.send_message(message.chat.id, "Выберите группу куда перенести пользователя", reply_markup=keyboard)
        bot.register_next_step_handler(g, branch2)

    elif message.text == 'ФИО':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Отмена']])
        fio = bot.send_message(message.chat.id, "Напишите новое имя для пользователя", reply_markup=keyboard)
        bot.register_next_step_handler(fio, branch2)


def branch2(message):
    groups = MySqlGroup.groups('')

    if message.text == 'Сгенерировать':

        MySqlUsers.edit_user(edit_user, 'password', '')
        password = MySqlUsers.UsersPassword(edit_user)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать', 'Информация', 'Редактировать']])
        bot.send_message(message.chat.id, "Пароль сгенирирован: {p}".format(p=password), reply_markup=keyboard)

    elif message.text in groups:
        MySqlUsers.edit_user(edit_user, 'group', message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать', 'Информация', 'Редактировать']])
        bot.send_message(message.chat.id, "Новая группа для {u}: {g}".format(u=edit_user, g=message.text),
                         reply_markup=keyboard)

    elif message.text == 'Отмена':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать', 'Информация', 'Редактировать']])
        bot.send_message(message.chat.id, "Последнее действие отменено".format(u=edit_user, g=message.text),
                         reply_markup=keyboard)

    else:
        MySqlUsers.edit_user(edit_user, 'fio', message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(command) for command in ['Создать', 'Информация', 'Редактировать']])
        bot.send_message(message.chat.id, "ФИО для {u}: {fio}".format(u=edit_user, fio=message.text),
                         reply_markup=keyboard)
'''
@bot.message_handler(func=lambda m: m.entities and 
                                    (m.chat.type == 'group' or 
                                        m.chat.type == 'supergroup')   )
'''


@bot.callback_query_handler(func=lambda callback: True)
def inline(callback):
    groups = MySqlGroup.groups('')

    users = MySqlUsers.UsersName()

    if callback.data == 'Группы':

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in groups])
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text="Выберите группу", reply_markup=keyboard)

    if callback.data in groups:
        users_in_group = MySqlGroup.groups(callback.data)
        if users_in_group == []:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(*[types.InlineKeyboardButton(text=user, callback_data=user) for user in ['◀️ Назад']])
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  text="Нет пользователей в {group}".format(group=callback.data), reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(*[types.InlineKeyboardButton(text=user, callback_data=user) for user in users_in_group])
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  text="Выберите пользователя", reply_markup=keyboard)

    elif callback.data in users:
        keyboard = types.InlineKeyboardMarkup()
        global USER
        USER = callback.data
        keyboard.add(*[types.InlineKeyboardButton(text=choose, callback_data=choose) for choose in ['Пароль', 'Информация']])
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text="Вывести пароль пользователя или информацию?", reply_markup=keyboard)

    elif callback.data == 'Информация':

        user = MySqlUsers.UserInfo(USER)
        keyboard = types.InlineKeyboardMarkup()
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text="Пользователь: *{data}* \nУстройства: \n*{userInfo}*".format(data=USER, userInfo=user),
                              reply_markup=keyboard, parse_mode="Markdown")

    elif callback.data == 'Пароль':
        password = MySqlUsers.UsersPassword(USER)
        keyboard = types.InlineKeyboardMarkup()
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text="Пользователь: *{data}* \nПароль: *{passInfo}*".format(data=USER, passInfo=password),
                              reply_markup=keyboard, parse_mode="Markdown")

    elif callback.data == '❌':
        MySqlUsers.set_status(edit_user, 'off')
        status = MySqlUsers.get_status(edit_user)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=s, callback_data=s) for s in '✅'])
        bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,
                              text="Пользователь: {u} \nСтатус: {s}".format(u=edit_user, s=status),
                              reply_markup=keyboard)

    elif callback.data == '✅':
        MySqlUsers.set_status(edit_user, 'on')
        status = MySqlUsers.get_status(edit_user)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=s, callback_data=s) for s in '❌'])
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text="Пользователь: {u} \nСтатус: {s}".format(u=edit_user, s=status),
                              reply_markup=keyboard)

    elif callback.data == '◀️ Назад':
        callback.data = 'Группы'
        inline(callback)


bot.polling(none_stop=True, interval=0)
