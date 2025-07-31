import sqlite3


def add_new_task(con, task):
    """
    Query tasks by user_id
    :param cur: the Connection object
    :param user_id: user id
    :return: rows tasks
    """
    sql = """INSERT INTO tasks(title, description,
              status_id, user_id)
              VALUES (?, ?, ?, ?)
          """
    cur = con.cursor()
    try:
        cur.execute(sql, task)
        con.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()


if __name__ == "__main__":
    with sqlite3.connect("task.db") as con:
        add_new_task(con, ("Task New Test", "Task Description", 1, 1))
