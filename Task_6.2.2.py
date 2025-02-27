import sqlite3
from sqlite3 import Error

# Funkcja do tworzenia połączenia z bazą danych
def create_connection(db_file):
    """Utwórz połączenie z bazą danych SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z bazą danych: {db_file}, wersja SQLite: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn

# Funkcja do wykonywania skryptów SQL
def execute_sql(conn, sql):
    """Wykonaj skrypt SQL."""
    try:
        c = conn.cursor()
        c.execute(sql)
        print("Skrypt SQL wykonany pomyślnie.")
    except Error as e:
        print(e)

# Funkcja do dodawania projektu
def add_project(conn, project):
    """Dodaj nowy projekt do tabeli projects."""
    sql = '''INSERT INTO projects(nazwa, start_date, end_date) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

# Funkcja do dodawania zadania
def add_task(conn, task):
    """Dodaj nowe zadanie do tabeli tasks."""
    sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

# Funkcja do aktualizacji danych
def update(conn, table, id, **kwargs):
    """Aktualizuj rekord w tabeli."""
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )

    sql = f'''UPDATE {table} SET {parameters} WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Rekord zaktualizowany pomyślnie.")
    except sqlite3.OperationalError as e:
        print(e)

# Funkcja do usuwania danych
def delete_where(conn, table, **kwargs):
    """Usuń rekordy z tabeli na podstawie warunków."""
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Rekordy usunięte pomyślnie.")

def delete_all(conn, table):
    """Usuń wszystkie rekordy z tabeli."""
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Wszystkie rekordy usunięte pomyślnie.")

# Główna funkcja programu
def main():
    db_file = "database.db"

    # Skrypty SQL do tworzenia tabel
    create_projects_sql = """
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        nazwa text NOT NULL,
        start_date text,
        end_date text
    );
    """

    create_tasks_sql = """
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

    # Połączenie z bazą danych i utworzenie tabel
    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_projects_sql)
        execute_sql(conn, create_tasks_sql)

        # Dodanie przykładowego projektu i zadania
        project = ("Powtórka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
        project_id = add_project(conn, project)

        task = (
            project_id,
            "Czasowniki regularne",
            "Zapamiętaj czasowniki ze strony 30",
            "started",
            "2020-05-11 12:00:00",
            "2020-05-11 15:00:00"
        )
        task_id = add_task(conn, task)
        print(f"Dodano projekt o ID: {project_id} i zadanie o ID: {task_id}")

        # Aktualizacja zadania
        update(conn, "tasks", task_id, status="completed")
        print("Zaktualizowano status zadania.")

        # Usunięcie zadania
        delete_where(conn, "tasks", id=task_id)
        print("Usunięto zadanie.")

        # Usunięcie wszystkich zadań (opcjonalnie)
        # delete_all(conn, "tasks")

        # Zamknięcie połączenia
        conn.close()
    else:
        print("Błąd! Nie można połączyć z bazą danych.")

if __name__ == "__main__":
    main()