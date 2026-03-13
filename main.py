from psycopg2.errors import UniqueViolation
import cli, db

conn, cur = db.connection_db()
db.create_db(cur)


def add_user():
    name = str(input('user -> '))
    age = int(input('age -> '))
    is_admin = cli.ask_yes_no('admin?')

    try:
        db.add_user_db(cur, name, age, is_admin)
    except UniqueViolation:
        conn.rollback()
        print('такой юзер уже есть')

    conn.commit()

def delete_user():
    column = input('по какому столбцу удалить? (id/name/age) -> ')
    value = input('значение -> ')

    db.delete_user_db(cur, column, value)
    print('deleted')

    conn.commit()

def login():
    name = input('name -> ')
    age = int(input('age -> '))
    db.login_db(cur, name, age)

def admin_menu():

    print("""
1 удалить пользователя
2 изменить пользователя
3 показать пользователей
""")


conn.commit()
cur.close()
conn.close()


