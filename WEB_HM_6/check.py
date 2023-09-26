import sqlite3


def is_table_empty(table_name):
    conn = sqlite3.connect('school.db')
    cur = conn.cursor()

    cur.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cur.fetchone()[0]

    conn.close()
    print(count)
    return count == 0


# Перевірка заповненості таблиці students
if is_table_empty('students'):
    print('Таблиця students пуста')
else:
    print('Таблиця students містить дані')


result = is_table_empty('students')