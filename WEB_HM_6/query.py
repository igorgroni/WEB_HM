import sqlite3


def execute_query(num: int) -> list:
    num = str(num)
    query = f'query_{num}.sql'
    with open(query, 'r') as f:
        sql = f.read()
        print(sql)

    with sqlite3.connect('school.db') as con:
        cursor = con.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


if __name__ == "__main__":
    for i in range(10):
        print(execute_query(i + 1))
