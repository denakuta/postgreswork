from psycopg2.errors import UniqueViolation
import cli, db

conn, cur = db.connection_db()
db.create_db(cur)


def admin_menu():
    print("""
1 удалить пользователя
2 изменить пользователя
3 показать пользователей
4 выход
""")


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


def show_users():
    users = db.get_all_users_db(cur)
    for user in users:
        print(f"ID: {user[0]}, name: {user[1]}, age: {user[2]}, admin: {user[3]}")
    conn.commit()


def user_menu(user):
    print(f"\nwelcome, {user[1]}!")
    while True:
        if user[3]:  # is_admin
            admin_menu()
            choice = input('--> ')
            if choice == '1':
                delete_user()
            elif choice == '2':
                update_user()
            elif choice == '3':
                show_users()
            elif choice == '4':
                break
            else:
                print('неверный выбор')
        else:
            print("""
1. посмотреть профиль
2. выход
""")
            choice = input('--> ')
            if choice == '1':
                print(f"ID: {user[0]}, Имя: {user[1]}, Возраст: {user[2]}, Админ: {user[3]}")
            elif choice == '2':
                break
            else:
                print('неверный выбор')



def login():
    name = input('name -> ')
    age = int(input('age -> '))
    user = db.login_db(cur, name, age)

    if user:
        user_menu(user)
    else:
        print('пользователь не найден')


def update_user():
    name = input('name who u want to edit -> ')
    age = int(input('new age ->'))
    is_admin = cli.ask_yes_no('admin?')
    db.update_user_db(cur, age, is_admin, name)
    print('user updated')


choice = input('1. registration\n2. login\n3. exit\n--> ')
if choice == '1':
    add_user()
    print('user added')

elif choice == '2':
    login()

elif choice == '3':
    print('до свидания!')

else:
    print('неверный выбор')

conn.commit()
cur.close()
conn.close()
