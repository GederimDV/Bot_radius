# -*-coding:utf-8-*-
import MySQLdb
import MySQLdb.cursors
from configs import sql


""" Указать пользователя = показать всю информацию по нему, пустой аргумент = все пользователи """

def UserInfo(u):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)  ###Подключение к БД
    cursor = db.cursor()
    col = cursor.execute("CALL `get_users`('{u}', '');".format(u=u))  ###Выполнение команды
    row = cursor.fetchall()

    user = []
    for j in range(col):
        user.append(row[j])
    inf = ''
    for i in range(col):
        if user[i]['mac'] == None:
            inf = "Нет устройств"
        else:
            inf += "MAC: " + user[i]['mac'] + "\nName_SW: " + user[i]['sw_name'] + "\nIP_SW: " + user[i]['switch'] + "\nТип: "\
                   + user[i]['type'] + "\nПорт: " + user[i]['port'] + "\n------------------------------\n"
    db.close()
    return inf


def UsersPassword(u):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)  ###Подключение к БД
    cursor = db.cursor()
    col = cursor.execute("CALL `get_users`('{u}', '{p}');".format(u=u, p='password'))  ###Выполнение команды
    row = cursor.fetchall()

    userPass = []
    for j in range(col):
        userPass.append(row[j])
    db.close()
    UsersPass = ''
    for i in range(col):
        UsersPass += userPass[i]['password'] + "\n"
    return UsersPass


def UsersName():
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)  ###Подключение к БД
    cursor = db.cursor()
    col = cursor.execute("CALL `get_users`('', '');")  ###Выполнение команды

    row = cursor.fetchall()
    #print(row)
    user = []
    for j in range(col):
        user.append(row[j]['username'])
    #print(user)
    db.close()
    return user


"""Получение информации, группы, логина, пароля и ФИО пользователя"""


def details_users(user):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)  ###Подключение к БД
    cursor = db.cursor()
    col = cursor.execute("CALL `get_users`('{u}', 'details');".format(u=user))  ###Выполнение команды

    row = cursor.fetchall()
    details = 'Пользователь: ' + row[0]['username'] + '\n' + 'ФИО: ' + row[0]['fio'] + '\n' + 'Группа: '\
             + row[0]['comment'] + '\n' + 'Пароль: ' + row[0]['password']
    #print(row)
    return details


def get_status(user):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)  ###Подключение к БД
    cursor = db.cursor()
    cursor.execute("CALL `get_users`('{u}', 'status');".format(u=user))  ###Выполнение команды

    row = cursor.fetchall()
    status = row[0]['block']
    print(row[0]['block'])
    if status == 1:
        status = '❌'
    elif status == 0:
        status = '✅'

    db.close()
    return status


def set_status(user, on_off):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)

    cursor = db.cursor()
    cursor.execute("CALL `set_user_status`('{u}', '{of}');".format(u=user, of=on_off))

    db.commit()
    db.close()


def create_user(email, fio, group):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)

    cursor = db.cursor()
    cursor.execute("CALL `create_user`('{e}', '{f}', '{g}');".format(e=email, f=fio, g=group))

    db.commit()
    db.close()


def edit_user(username, menu, value):
    '''
    1) password - сгенерить новый пароль
    2) group - сменить группу
    3) fio - сменить ФИО
    '''
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)

    cursor = db.cursor()
    cursor.execute("CALL `edit_user`('{u}', '{m}', '{v}');".format(u=username, m=menu, v=value))

    db.commit()
    db.close()


#create_user(email=input(), fio=input(), group=input())
