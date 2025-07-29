import sqlite3


def update_task(conn: sqlite3.Connection, status_id: int, id: int):
    """
    Update status_id of a task.
    :param conn: SQLite connection object
    :param status_id: New status ID to set
    :param id: ID of the task to update
    :return:
    """
    sql = """
    UPDATE tasks
    SET status_id = ?
    WHERE id = ?
    """
    cur = conn.cursor()
    try:
        cur.execute(sql, (status_id, id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()


if __name__ == "__main__":
    with sqlite3.connect("task.db") as con:
        update_task(con, 1, 3)
