import sqlite3

DB_PATH = "vaultos.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def load_notes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM notes ORDER BY id ASC")
    rows = cursor.fetchall()

    conn.close()

    return {f"id_{row[0]}": row[1] for row in rows}


def get_note_by_id(note_id):
    if not note_id:
        return None
    if not note_id.startswith("id_"):
        return None
    
    numeric_id = int(note_id.replace("id_", ""))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT title, body FROM notes WHERE id = ?", (numeric_id,))
    note = cursor.fetchone()

    conn.close()
    return note


def create_note(title, body):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (title, body, created_at) VALUES (?, ?, datetime('now'))",
        (title, body)
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return f"id_{new_id}"


def update_note(note_id, title, body):
    numeric_id = int(note_id.replace("id_", ""))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET title = ?, body = ? WHERE id = ?",
        (title, body, numeric_id)
    )

    conn.commit()
    conn.close()


def delete_note(note_id):
    numeric_id = int(note_id.replace("id_", ""))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?", (numeric_id,))

    conn.commit()
    conn.close()
