from models.space_object import SpaceObject
from models.observation_system import ObservationSystem
from models.observation import Observation
from models.conjunction import Conjunction
from models.notification import Notification
from models.report import Report


class MainController:

    def __init__(self, database):
        self.database = database

    # =================================
    # КОСМИЧЕСКИЕ ОБЪЕКТЫ
    # =================================

    def add_space_object(
        self,
        catalog_number,
        international_id,
        object_type,
        size,
        x,
        y,
        z,
        vx,
        vy,
        vz
    ):
        space_object = SpaceObject(
            catalog_number,
            international_id,
            object_type,
            float(size),
            float(x),
            float(y),
            float(z),
            float(vx),
            float(vy),
            float(vz)
        )

        self.database.execute("""
            INSERT INTO space_objects (
                catalog_number,
                international_id,
                object_type,
                size,
                x,
                y,
                z,
                vx,
                vy,
                vz,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            space_object.catalog_number,
            space_object.international_id,
            space_object.object_type,
            space_object.size,
            space_object.x,
            space_object.y,
            space_object.z,
            space_object.vx,
            space_object.vy,
            space_object.vz,
            space_object.status
        ))

    def get_space_objects(self):
        return self.database.fetch_all("""
            SELECT
                id,
                catalog_number,
                international_id,
                object_type,
                size,
                x,
                y,
                z,
                vx,
                vy,
                vz,
                status
            FROM space_objects
        """)

    def mark_object_as_lost(self, object_id):
        self.database.execute("""
            UPDATE space_objects
            SET status = 'lost'
            WHERE id = ?
        """, (
            object_id,
        ))

    def mark_object_as_found(self, object_id):
        self.database.execute("""
            UPDATE space_objects
            SET status = 'active'
            WHERE id = ?
        """, (
            object_id,
        ))

    def delete_space_object(self, object_id):

        self.database.execute("""
            DELETE FROM notifications
            WHERE conjunction_id IN (
                SELECT id
                FROM conjunctions
                WHERE object1_id = ?
                   OR object2_id = ?
            )
        """, (
            object_id,
            object_id
        ))

        self.database.execute("""
            DELETE FROM conjunctions
            WHERE object1_id = ?
               OR object2_id = ?
        """, (
            object_id,
            object_id
        ))

        self.database.execute("""
            DELETE FROM observations
            WHERE space_object_id = ?
        """, (
            object_id,
        ))

        self.database.execute("""
            DELETE FROM space_objects
            WHERE id = ?
        """, (
            object_id,
        ))

    # =================================
    # СРЕДСТВА НАБЛЮДЕНИЯ
    # =================================

    def add_observation_system(
        self,
        name,
        system_type,
        coverage_area,
        sensitivity
    ):
        system = ObservationSystem(
            name,
            system_type,
            coverage_area,
            float(sensitivity)
        )

        self.database.execute("""
            INSERT INTO observation_systems (
                name,
                system_type,
                coverage_area,
                sensitivity,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            system.name,
            system.system_type,
            system.coverage_area,
            system.sensitivity,
            system.status
        ))

    def get_observation_systems(self):
        return self.database.fetch_all("""
            SELECT *
            FROM observation_systems
        """)

    # =================================
    # НАБЛЮДЕНИЯ
    # =================================

    def add_observation(
        self,
        space_object_id,
        observation_system_id,
        date_time,
        orbital_data
    ):
        observation = Observation(
            int(space_object_id),
            int(observation_system_id),
            date_time,
            orbital_data
        )

        observation.validate_data()

        self.database.execute("""
            INSERT INTO observations (
                space_object_id,
                observation_system_id,
                date_time,
                orbital_data
            )
            VALUES (?, ?, ?, ?)
        """, (
            observation.space_object_id,
            observation.observation_system_id,
            observation.date_time,
            observation.orbital_data
        ))

    # =================================
    # РАСЧЁТ СБЛИЖЕНИЙ
    # =================================

    def calculate_conjunctions(self):

        rows = self.database.fetch_all("""
            SELECT
                id,
                catalog_number,
                x,
                y,
                z,
                vx,
                vy,
                vz
            FROM space_objects
            WHERE status = 'active'
        """)

        objects = []

        for row in rows:
            objects.append({
                "id": row[0],
                "catalog_number": row[1],
                "x": row[2],
                "y": row[3],
                "z": row[4],
                "vx": row[5],
                "vy": row[6],
                "vz": row[7]
            })

        results = []

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):

                object1 = objects[i]
                object2 = objects[j]

                conjunction = Conjunction(
                    object1,
                    object2
                )

                conjunction.calculate()

                conjunction_id = self.database.execute("""
                    INSERT INTO conjunctions (
                        object1_id,
                        object2_id,
                        closest_time,
                        minimum_distance,
                        collision_probability,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    object1["id"],
                    object2["id"],
                    conjunction.closest_time,
                    conjunction.minimum_distance,
                    conjunction.collision_probability,
                    conjunction.status
                ))

                results.append({
                    "id": conjunction_id,
                    "object1": object1["catalog_number"],
                    "object2": object2["catalog_number"],
                    "time": conjunction.closest_time,
                    "distance": conjunction.minimum_distance,
                    "probability": conjunction.collision_probability,
                    "status": conjunction.status
                })

        return results

    def get_conjunctions(self):
        return self.database.fetch_all("""
            SELECT
                conjunctions.id,
                o1.catalog_number,
                o2.catalog_number,
                conjunctions.closest_time,
                conjunctions.minimum_distance,
                conjunctions.collision_probability,
                conjunctions.status
            FROM conjunctions

            JOIN space_objects AS o1
            ON conjunctions.object1_id = o1.id

            JOIN space_objects AS o2
            ON conjunctions.object2_id = o2.id
        """)

    # =================================
    # УВЕДОМЛЕНИЯ
    # =================================

    def create_notification(
        self,
        conjunction_id,
        owner_name,
        message
    ):
        notification = Notification(
            int(conjunction_id),
            owner_name,
            message
        )

        notification.send_notification()

        self.database.execute("""
            INSERT INTO notifications (
                conjunction_id,
                owner_name,
                message,
                status,
                response
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            notification.conjunction_id,
            notification.owner_name,
            notification.message,
            notification.status,
            notification.response
        ))

    # =================================
    # ОТЧЁТЫ
    # =================================

    def get_report(self):

        report = Report(
            self.database
        )

        return {
            "objects":
                report.generate_objects_report(),

            "conjunctions":
                report.generate_conjunction_report(),

            "dangerous":
                report.generate_dangerous_report(),

            "lost":
                report.generate_lost_objects_report()
        }