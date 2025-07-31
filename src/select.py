import sqlite3


def select_task_by_id(cur: sqlite3.Cursor, user_id: int):
    """
    Query tasks by user_id
    :param cur: the Connection object
    :param user_id: user id
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_task_by_status(cur: sqlite3.Cursor, status_id: int):
    """
    Query tasks by status_id
    :param cur: the Connection object
    :param status_id: status id
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute("SELECT * FROM tasks WHERE status_id=?", (status_id,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_user_with_out_tasks(cur: sqlite3.Cursor):
    """
    Query users with out tasks
    :param cur: the Connection object
    :return: rows users
    """
    rows = None
    try:
        cur.execute(
            "SELECT * FROM user WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL)"
        )
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_task_with_uncompleted(cur: sqlite3.Cursor):
    """
    Query tasks that are uncompleted
    :param cur: the Connection object
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute("SELECT * FROM tasks WHERE status_id = 2 OR status_id = 1")
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return


def select_user_by_email_pattern(cur: sqlite3.Cursor, email_pattern: str):
    """
    Query users by email pattern
    :param cur: the Connection object
    :param email_pattern: email pattern
    :return: rows users
    """
    rows = None
    try:
        cur.execute("SELECT * FROM user WHERE email LIKE ?", (email_pattern,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_task_count_by_group_from_status(cur: sqlite3.Cursor):
    """
    Query task count by group from status
    :param cur: the Connection object
    :return: task count
    """
    count = None
    try:
        cur.execute(
            """
            SELECT s.name as status_name, COUNT(t.status_id) as task_count 
            FROM tasks t
            JOIN status s ON t.status_id = s.id
            GROUP BY t.status_id, s.name
            ORDER BY t.status_id
        """
        )
        count = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return count


def select_task_by_email_user_pattern(cur: sqlite3.Cursor, email_pattern: str):
    """
    Query tasks by user email pattern
    :param cur: the Connection object
    :param email_pattern: email pattern
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute(
            """
            SELECT t.id, t.title, t.description, t.status_id, t.user_id 
            FROM tasks t
            JOIN user u ON t.user_id = u.id
            WHERE u.email LIKE ?
        """,
            (email_pattern,),
        )
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_task_with_out_description(cur: sqlite3.Cursor):
    """
    Query tasks with out description
    :param cur: the Connection object
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute(
            """
            SELECT * FROM tasks t
            WHERE t.description = ''
        """
        )
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_task_by_status_with_user_group(cur: sqlite3.Cursor, status_id: int):
    """
    Query tasks by status
    :param cur: the Connection object
    :param status_id: task status id
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute(
            """
            SELECT * FROM tasks t
            WHERE t.description = ''
        """
        )
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_users_with_tasks_by_status(cur: sqlite3.Cursor, status_id: int):
    """
    Query users with their tasks by status
    :param cur: the Connection object
    :param status_id: status id
    :return: list of users with tasks
    """
    try:
        # Получаем все данные одним запросом
        cur.execute(
            """
            SELECT u.id, u.fullname, u.email,
                   t.id as task_id, t.title, t.description
            FROM user u
            INNER JOIN tasks t ON u.id = t.user_id 
            WHERE t.status_id = ?
            ORDER BY u.id
        """,
            (status_id,),
        )

        rows = cur.fetchall()

        # Группируем данные по пользователям
        users_dict = {}
        for row in rows:
            user_id = row[0]
            if user_id not in users_dict:
                users_dict[user_id] = {
                    "id": row[0],
                    "fullname": row[1],
                    "email": row[2],
                    "tasks": [],
                }

            # Добавляем задачу к пользователю
            users_dict[user_id]["tasks"].append(
                {
                    "id": row[3],
                    "title": row[4],
                    "description": row[5],
                }
            )

        # Преобразуем словарь в список
        return list(users_dict.values())

    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
        return []
    finally:
        cur.close()


def select_all_users(cur: sqlite3.Cursor):
    """
    Query users
    :param cur: the Connection object
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute(
            """
            SELECT u.*, COUNT(t.id) as count_task FROM user u
            LEFT JOIN tasks t ON t.user_id = u.id
            GROUP BY u.id
        """
        )
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


if __name__ == "__main__":
    with sqlite3.connect("task.db") as con:
        cur = con.cursor()
        # print("tasks:")
        # tasks = select_task_by_id(cur, 2)
        # print(tasks)

        # print("tasks by status:")
        # tasks_by_status = select_task_by_status(cur, 1)
        # print(tasks_by_status)

        # uncompleted_task = select_task_with_uncompleted(cur)
        # print(uncompleted_task)

        # user_by_email = select_user_by_email_pattern(cur, "%@example.org")
        # print(user_by_email)

        # task_by_group = select_task_count_by_group_from_status(cur)
        # print(task_by_group)

        # tasks_by_email = select_task_by_email_user_pattern(cur, "%@example.org")
        # print(tasks_by_email)

        # tasks_with_out_description = select_task_with_out_description(cur)
        # print(tasks_with_out_description)

        # data = select_users_with_tasks_by_status(cur, 1)
        # print(data)

        user = select_all_users(cur)
        print(user)
