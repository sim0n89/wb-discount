from mysql.connector import MySQLConnection, Error
import mysql.connector
from config import host, USER, passwd, database
from datetime import date
import traceback

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def check_product(id):
    sql = f"SELECT id from products where market_id={str(id)}"
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql)
    have = cursor.fetchall()
    cursor.close()
    conn.close()
    if have == []:
        return False
    else:
        return have

def new_product(id, price):
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor(buffered=True)
    sql = f"INSERT INTO products (market_id) VALUES ({id})"
    cursor.execute(sql)
    conn.commit()
    try:
        sql = "SELECT LAST_INSERT_ID() from products"
        cursor.execute(sql)
        maxId = cursor.fetchone()
        sql = "INSERT INTO prices (prId, price, date) VALUES (%s, %s, %s)"
        val = (maxId[0], str(price), date.today())

        cursor.execute(sql, val)
        conn.commit()
    except Exception:
        traceback.print_exc()
    cursor.close()
    conn.close()


def add_new_price(prId, price):
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor(buffered=True)
    sql = "INSERT INTO prices (prId, price, date) VALUES (%s, %s, %s)"
    val = (prId, str(price), date.today())
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()


def get_prices(prId):
    sql = f"SELECT * from prices WHERE prId = {prId}"
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql)
    prices = cursor.fetchall()
    cursor.close()
    conn.close()
    return prices


def check_root(id):
    print(id)
    sql = f"SELECT * from roots where root={str(id)}"
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql)
    have = cursor.fetchone()
    cursor.close()
    conn.close()
    if have == None:
        return True
    else:
        return False

def add_root(id):
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor(buffered=True)
    sql = f"INSERT INTO roots (root) VALUES ({id})"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def clear_root():
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor(buffered=True)
    sql = 'TRUNCATE roots'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()