import sqlite3


def select_task_by_id(cur, user_id):
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


def select_task_by_status(cur, status_id):
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


def select_user_with_out_tasks(cur):
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


if __name__ == "__main__":
    with sqlite3.connect("task.db") as con:
        cur = con.cursor()
        # print("tasks:")
        # tasks = select_task_by_id(cur, 2)
        # print(tasks)

        print("tasks by status:")
        tasks_by_status = select_task_by_status(cur, 1)
        print(tasks_by_status)
