import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "space_monitoring.db"


class Database:

    def __init__(self):
        self.db_name = DB_PATH

        print("База данных:", self.db_name)

        self.check_database_structure()
        self.create_tables()

    def connect(self):
        connection = sqlite3.connect(self.db_name)

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    # =========================================
    # ПРОВЕРКА СТРУКТУРЫ БАЗЫ
    # =========================================

    def check_database_structure(self):

        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            "PRAGMA foreign_keys = OFF"
        )

        # ---------------------------------
        # Проверяем space_objects
        # ---------------------------------

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'space_objects'
        """)

        if cursor.fetchone():

            cursor.execute("""
                PRAGMA table_info(space_objects)
            """)

            columns = {
                row[1]
                for row in cursor.fetchall()
            }

            required_columns = {
                "id",
                "catalog_number",
                "international_id",
                "object_type",
                "size",
                "x",
                "y",
                "z",
                "vx",
                "vy",
                "vz",
                "status"
            }

            if not required_columns.issubset(columns):

                print(
                    "Обнаружена старая таблица "
                    "space_objects. Пересоздание..."
                )

                cursor.execute("""
                    DROP TABLE IF EXISTS notifications
                """)

                cursor.execute("""
                    DROP TABLE IF EXISTS conjunctions
                """)

                cursor.execute("""
                    DROP TABLE IF EXISTS observations
                """)

                cursor.execute("""
                    DROP TABLE IF EXISTS space_objects
                """)

        # ---------------------------------
        # Проверяем conjunctions
        # ---------------------------------

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'conjunctions'
        """)

        if cursor.fetchone():

            cursor.execute("""
                PRAGMA table_info(conjunctions)
            """)

            columns = {
                row[1]
                for row in cursor.fetchall()
            }

            required_columns = {
                "id",
                "object1_id",
                "object2_id",
                "closest_time",
                "minimum_distance",
                "collision_probability",
                "status"
            }

            if not required_columns.issubset(columns):

                print(
                    "Обнаружена старая таблица "
                    "conjunctions. Пересоздание..."
                )

                cursor.execute("""
                    DROP TABLE IF EXISTS notifications
                """)

                cursor.execute("""
                    DROP TABLE IF EXISTS conjunctions
                """)

        connection.commit()
        connection.close()

    # =========================================
    # СОЗДАНИЕ ТАБЛИЦ
    # =========================================

    def create_tables(self):

        with self.connect() as connection:

            cursor = connection.cursor()

            # ---------------------------------
            # КОСМИЧЕСКИЕ ОБЪЕКТЫ
            # ---------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS space_objects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    catalog_number TEXT UNIQUE NOT NULL,
                    international_id TEXT,

                    object_type TEXT NOT NULL,
                    size REAL NOT NULL,

                    x REAL NOT NULL,
                    y REAL NOT NULL,
                    z REAL NOT NULL,

                    vx REAL NOT NULL,
                    vy REAL NOT NULL,
                    vz REAL NOT NULL,

                    status TEXT NOT NULL
                )
            """)

            # ---------------------------------
            # СРЕДСТВА НАБЛЮДЕНИЯ
            # ---------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS observation_systems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    name TEXT NOT NULL,
                    system_type TEXT NOT NULL,

                    coverage_area TEXT,
                    sensitivity REAL,

                    status TEXT NOT NULL
                )
            """)

            # ---------------------------------
            # НАБЛЮДЕНИЯ
            # ---------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    space_object_id INTEGER NOT NULL,
                    observation_system_id INTEGER NOT NULL,

                    date_time TEXT NOT NULL,
                    orbital_data TEXT,

                    FOREIGN KEY (space_object_id)
                        REFERENCES space_objects(id),

                    FOREIGN KEY (observation_system_id)
                        REFERENCES observation_systems(id)
                )
            """)

            # ---------------------------------
            # СБЛИЖЕНИЯ
            # ---------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conjunctions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    object1_id INTEGER NOT NULL,
                    object2_id INTEGER NOT NULL,

                    closest_time REAL NOT NULL,

                    minimum_distance REAL NOT NULL,

                    collision_probability REAL NOT NULL,

                    status TEXT NOT NULL,

                    FOREIGN KEY (object1_id)
                        REFERENCES space_objects(id),

                    FOREIGN KEY (object2_id)
                        REFERENCES space_objects(id)
                )
            """)

            # ---------------------------------
            # УВЕДОМЛЕНИЯ
            # ---------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    conjunction_id INTEGER NOT NULL,

                    owner_name TEXT NOT NULL,

                    message TEXT NOT NULL,

                    status TEXT NOT NULL,

                    response TEXT,

                    FOREIGN KEY (conjunction_id)
                        REFERENCES conjunctions(id)
                )
            """)

            connection.commit()

    # =========================================
    # ВЫПОЛНЕНИЕ SQL
    # =========================================

    def execute(
        self,
        query,
        params=()
    ):

        with self.connect() as connection:

            cursor = connection.cursor()

            cursor.execute(
                query,
                params
            )

            connection.commit()

            return cursor.lastrowid

    # =========================================
    # ПОЛУЧЕНИЕ НЕСКОЛЬКИХ СТРОК
    # =========================================

    def fetch_all(
        self,
        query,
        params=()
    ):

        with self.connect() as connection:

            cursor = connection.cursor()

            cursor.execute(
                query,
                params
            )

            return cursor.fetchall()

    # =========================================
    # ПОЛУЧЕНИЕ ОДНОЙ СТРОКИ
    # =========================================

    def fetch_one(
        self,
        query,
        params=()
    ):

        with self.connect() as connection:

            cursor = connection.cursor()

            cursor.execute(
                query,
                params
            )

            return cursor.fetchone()