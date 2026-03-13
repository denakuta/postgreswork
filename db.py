from psycopg2 import sql
import psycopg2

def connection_db():
    conn = psycopg2.connect(
        dbname="testdb",
        user="denakuta",
        password="qwe",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    return conn, cur

def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id   SERIAL PRIMARY KEY,
        name VARCHAR(15) UNIQUE NOT NULL,
        age INT CHECK (age > 0),
        is_admin BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP(0) DEFAULT NOW()
    );""")

def add_user_db(cur, name, age, is_admin):
    cur.execute("INSERT INTO users (name, age, is_admin)"
                "VALUES (%s, %s, %s) RETURNING id;",
                (name, age, is_admin,)
                )

    print(cur.fetchone()[0])

def delete_user_db(cur, column, value):
    allowed_columns = ['id', 'name', 'age']

    if column not in allowed_columns:
        raise ValueError('неправильный выбор')

    query = sql.SQL('DELETE FROM users WHERE {} = %s').format(
        sql.Identifier(column)
    )

    cur.execute(query, (value, ))

def login_db(cur, name, age):
    cur.execute(
        """
        SELECT id, name, age, is_admin
        FROM users
        WHERE name = %s AND age = %s
        """,
        (name, age)
    )
    return cur.fetchone()

def update_user_db(cur, age: int, is_admin: bool, name):
    cur.execute(
        "UPDATE users SET age = %s, is_admin = %s WHERE name = %s",
        (age, is_admin, name)
    )

def get_all_users_db(cur):
    cur.execute("SELECT id, name, age, is_admin FROM users")
    return cur.fetchall()

