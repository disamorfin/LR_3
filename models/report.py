class Report:
    def __init__(self, database):
        self.database = database

    def generate_objects_report(self):

        return self.database.fetch_all("""
            SELECT
                object_type,
                COUNT(*)

            FROM space_objects

            GROUP BY object_type
        """)

    def generate_conjunction_report(self):

        result = self.database.fetch_one("""
            SELECT COUNT(*)
            FROM conjunctions
        """)

        return result[0]

    def generate_dangerous_report(self):

        result = self.database.fetch_one("""
            SELECT COUNT(*)

            FROM conjunctions

            WHERE status = 'dangerous'
        """)

        return result[0]

    def generate_lost_objects_report(self):

        return self.database.fetch_all("""
            SELECT *

            FROM space_objects

            WHERE status = 'lost'
        """)