import sqlite3


def delete_task_by_id(cur: sqlite3.Cursor, id: int):
    """
    Delete tasks by id
    :param cur: the Connection object
    :param id: task id
    :return: rows tasks
    """
    rows = None
    try:
        cur.execute("DELETE FROM tasks WHERE id=?", (id,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
    return rows


if __name__ == "__main__":
    with sqlite3.connect("task.db") as con:
        cur = con.cursor()
        deleted_task = delete_task_by_id(cur, 3)
        print(f"Deleted task with id 3: {deleted_task}")
