import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Utwórz połączenie z bazą danych SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z bazą danych: {db_file}")
        return conn
    except Error as e:
        print(e)
    return conn

def execute_sql(conn, sql):
    """Wykonaj skrypt SQL."""
    try:
        c = conn.cursor()
        c.execute(sql)
        print("Skrypt SQL wykonany pomyślnie.")
    except Error as e:
        print(e)

if __name__ == "__main__":
    # Skrypty SQL do tworzenia tabel
    create_projects_sql = """
    -- Tabela projects
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        nazwa text NOT NULL,
        start_date text,
        end_date text
    );
    """

    create_tasks_sql = """
    -- Tabela tasks
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        project_id integer NOT NULL,
        nazwa VARCHAR(250) NOT NULL,
        opis TEXT,
        status VARCHAR(15) NOT NULL,
        start_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """

    db_file = "database.db"

    # Użycie context managera do połączenia z bazą danych
    with create_connection(db_file) as conn:
        if conn is not None:
            execute_sql(conn, create_projects_sql)
            execute_sql(conn, create_tasks_sql)
        else:
            print("Błąd! Nie można połączyć z bazą danych.")