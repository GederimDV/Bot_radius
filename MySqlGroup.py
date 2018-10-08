# -*-coding:utf-8-*-
import MySQLdb
import MySQLdb.cursors
from configs import sql

### Пустой аргумент = показывает все группы,
def groups(name_group):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)  ###Подключение к БД
    cursor = db.cursor()

    col = cursor.execute("CALL `get_groups`('{x}');".format(x=name_group))  ###Выполнение команды
    row = cursor.fetchall()
    groups = []
    if name_group == '':
        for j in range(col):
            groups.append(row[j]['groupname'])
        #print(groups)
    else:
        for j in range(col):
            groups.append(row[j]['username'])
        #print(groups)

    db.close()
    return groups


def create_group(name, comment):
    db = MySQLdb.connect(sql.get('ip'), sql.get('user'), sql.get('pass'), sql.get('bd'),
                         charset='utf8', use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)  ###Подключение к БД
    cursor = db.cursor()

    cursor.execute("CALL `create_group`('{name}', '{comment}');".format(name=name, comment=comment))

    db.commit()
    db.close()


#create_group(name=input(), comment=input())
