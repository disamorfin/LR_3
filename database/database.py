import sqlite3


class Database:
    def __init__(self, db_name="space_monitoring.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self.connect() as connection:
            cursor = connection.cursor()

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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conjunctions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    object1_id INTEGER NOT NULL,
                    object2_id INTEGER NOT NULL,
                    event_time TEXT NOT NULL,
                    minimum_distance REAL NOT NULL,
                    collision_probability REAL NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (object1_id)
                        REFERENCES space_objects(id),
                    FOREIGN KEY (object2_id)
                        REFERENCES space_objects(id)
                )
            """)

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

    def execute(self, query, params=()):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return cursor.lastrowid

    def fetch_all(self, query, params=()):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query, params=()):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()