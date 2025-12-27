import sqlite3


def get_connection(db_name="tasks.db"):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db(db_name="tasks.db"):
    conn = get_connection(db_name)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def create_task(title, description, due_date, status, db_name="tasks.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tasks (title, description, due_date, status)
        VALUES (?, ?, ?, ?)
        """,
        (title, description, due_date, status),
    )
    conn.commit()
    conn.close()


def get_all_tasks(db_name="tasks.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task_by_id(task_id, db_name="tasks.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("Select * from tasks where id = ? ", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_task(task_id, title, description, due_date, status, db_name="tasks.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, status = ?
        WHERE id = ?
        """,
        (title, description, due_date, status, task_id),
    )
    conn.commit()
    conn.close()


def delete_task(task_id, db_name="tasks.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
