import faker
from random import randint, choice
import sqlite3

NUMBER_USERS = 5
NUMBER_TASKS = 30


def generate_fake_data(number_users, number_tasks):
    fake_users = []  # here we will store users
    fake_tasks = []  # here we will store tasks

    fake_data = faker.Faker()

    # Create users with unique emails
    emails = set()
    for _ in range(number_users):
        # Generate unique email
        while True:
            email = fake_data.email()
            if email not in emails:
                emails.add(email)
                break

        fake_users.append((fake_data.name(), email))

    # Generate tasks
    for _ in range(number_tasks):
        title = fake_data.catch_phrase()
        description = fake_data.text(max_nb_chars=200)
        fake_tasks.append((title, description))

    return fake_users, fake_tasks


def prepare_data(users, tasks):
    # Prepare data for users
    for_users = []
    for user in users:
        for_users.append(user)  # (fullname, email)

    # Prepare data for tasks
    for_tasks = []
    status_ids = [1, 2, 3]  # new, in progress, completed

    for task in tasks:
        title, description = task
        status_id = choice(status_ids)
        user_id = randint(1, len(users))  # random user
        for_tasks.append((title, description, status_id, user_id))

    return for_users, for_tasks


def insert_data_to_db(users, tasks):
    # Create database connection
    with sqlite3.connect("task.db") as con:
        cur = con.cursor()

        # Insert users
        sql_to_users = """INSERT INTO user(fullname, email)
                          VALUES (?, ?)"""
        cur.executemany(sql_to_users, users)

        # Insert tasks
        sql_to_tasks = """INSERT INTO tasks(title, description,
                                           status_id, user_id)
                          VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_tasks, tasks)

        # Commit changes
        con.commit()
        print(f"Added {len(users)} users and {len(tasks)} tasks")


if __name__ == "__main__":
    users, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    prepared_users, prepared_tasks = prepare_data(users, tasks)
    insert_data_to_db(prepared_users, prepared_tasks)
