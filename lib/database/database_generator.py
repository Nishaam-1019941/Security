import sqlite3
from pathlib import Path


class WP2DatabaseGenerator:
    def __init__(self, database_file, overwrite=False, initial_data=False):
        self.database_file = Path(database_file)
        self.create_initial_data = initial_data
        self.database_overwrite = overwrite
        self.test_file_location()
        self.conn = sqlite3.connect(self.database_file)

    def generate_database(self):
        self.create_table_teachers()
        self.create_table_notes()
        self.create_table_questions()
        self.create_table_categories()
        if self.create_initial_data:
            self.insert_admin_user()
            self.insert_categories()
            self.insert_example_notes()

    def create_table_categories(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            omschrijving TEXT NOT NULL,
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP);
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Categories table created")

    def create_table_questions(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS questions (
            questions_id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            exam_question TEXT NOT NULL,            
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP,            
            FOREIGN KEY (note_id) REFERENCES notes (note_id));
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Questions table created")

    def create_table_notes(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS notes (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            note_source TEXT NOT NULL,
            is_public INTEGER NOT NULL DEFAULT 1,
            teacher_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            note TEXT NOT NULL,
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP,            
            FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id));
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Notes table created")

    def create_table_teachers(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name TEXT NOT NULL,
            username TEXT NOT NULL,
            teacher_password TEXT NOT NULL,
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_admin INTEGER NOT NULL DEFAULT 0);
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Teacher table created")

    def insert_admin_user(self):
        teachers = [
            ("admin", "admin", "admin", 1),
            ("Diederik de Vries", "vried", "geheimer", 0),
        ]
        insert_statement = "INSERT INTO teachers (display_name, username, teacher_password, is_admin) VALUES (?, ?, ?, ?);"
        self.__execute_many_transaction_statement(insert_statement, teachers)
        print("✅ Default teachers / users created")

    def insert_example_notes(self):
        note = (
            "INSERT INTO notes (title, note_source, is_public, teacher_id, category_id, note) VALUES "
            "('Leuk internetweetje', 'nrc van 1 nov', 1, 1, 1, 'wist je dat html echt iets betekent? namelijk hypertext mark up language');"
        )
        self.__execute_transaction_statement(note)
        print("✅ Demo note created")

    def insert_categories(self):
        categories = [
            ("Onboarding",),
            ("Programming Essentials",),
        ]
        insert_statement = "INSERT INTO categories (omschrijving) VALUES (?);"
        self.__execute_many_transaction_statement(insert_statement, categories)
        print("✅ Default categories created")

    # Transacties zijn duur, dat wil zeggen, ze kosten veel tijd en CPU kracht. Als je veel insert doet
    # bundel je ze in één transactie, of je gebruikt de SQLite executemany methode.
    def __execute_many_transaction_statement(
        self, create_statement, list_of_parameters=()
    ):
        c = self.conn.cursor()
        c.executemany(create_statement, list_of_parameters)
        self.conn.commit()

    def __execute_transaction_statement(self, create_statement, parameters=()):
        c = self.conn.cursor()
        c.execute(create_statement, parameters)
        self.conn.commit()

    def test_file_location(self):
        if not self.database_file.parent.exists():
            raise ValueError(
                f"Database file location {self.database_file.parent} does not exist"
            )
        if self.database_file.exists():
            if not self.database_overwrite:
                raise ValueError(
                    f"Database file {self.database_file} already exists, set overwrite=True to overwrite"
                )
            else:
                # Unlink verwijdert een bestand
                self.database_file.unlink()
                print("✅ Database already exists, deleted")
        if not self.database_file.exists():
            try:
                self.database_file.touch()
                print("✅ New database setup")
            except Exception as e:
                raise ValueError(
                    f"Could not create database file {self.database_file} due to error {e}"
                )


if __name__ == "__main__":
    my_path = Path(__file__).parent.resolve()
    project_root = my_path.parent.parent
    # Deze slashes komen uit de "Path" module. Dit is een module die je kan gebruiken
    # om paden te maken. Dit is handig omdat je dan niet zelf hoeft te kijken of je
    # een / (mac) of een \ (windows) moet gebruiken.
    database_path = project_root / "databases" / "testgpt.db"
    database_generator = WP2DatabaseGenerator(
        database_path, overwrite=True, initial_data=True
    )
    database_generator.generate_database()
