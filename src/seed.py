import faker
from random import randint, choice
import sqlite3

NUMBER_USERS = 5
NUMBER_TASKS = 30


def generate_fake_data(number_users, number_tasks):
    fake_users = []  # тут зберігатимемо користувачів
    fake_tasks = []  # тут зберігатимемо завдання

    fake_data = faker.Faker()

    # Створимо користувачів з унікальними email
    emails = set()
    for _ in range(number_users):
        # Генеруємо унікальний email
        while True:
            email = fake_data.email()
            if email not in emails:
                emails.add(email)
                break

        fake_users.append((fake_data.name(), email))

    # Згенеруємо завдання
    for _ in range(number_tasks):
        title = fake_data.catch_phrase()
        description = fake_data.text(max_nb_chars=200)
        fake_tasks.append((title, description))

    return fake_users, fake_tasks


def prepare_data(users, tasks):
    # Подготавливаем данные для users
    for_users = []
    for user in users:
        for_users.append(user)  # (fullname, email)

    # Подготавливаем данные для tasks
    for_tasks = []
    status_ids = [1, 2, 3]  # new, in progress, completed

    for task in tasks:
        title, description = task
        status_id = choice(status_ids)
        user_id = randint(1, len(users))  # случайный пользователь
        for_tasks.append((title, description, status_id, user_id))

    return for_users, for_tasks


def insert_data_to_db(users, tasks):
    # Создаем соединение с БД
    with sqlite3.connect("task.db") as con:
        cur = con.cursor()

        # Вставляем пользователей
        sql_to_users = """INSERT INTO user(fullname, email)
                          VALUES (?, ?)"""
        cur.executemany(sql_to_users, users)

        # Вставляем задачи
        sql_to_tasks = """INSERT INTO tasks(title, description,
                                           status_id, user_id)
                          VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_tasks, tasks)

        # Фиксируем изменения
        con.commit()
        print(f"Добавлено {len(users)} пользователей и {len(tasks)} задач")


if __name__ == "__main__":
    users, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    prepared_users, prepared_tasks = prepare_data(users, tasks)
    insert_data_to_db(prepared_users, prepared_tasks)
