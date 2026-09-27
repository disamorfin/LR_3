import math


class Conjunction:
    # Считаем сближение опасным,
    # если расстояние меньше 10 км
    DANGER_DISTANCE = 10.0

    # Анализируем следующие 24 часа
    MAX_TIME = 24 * 60 * 60

    def __init__(
        self,
        object1,
        object2
    ):
        self.object1 = object1
        self.object2 = object2

        self.closest_time = 0
        self.minimum_distance = 0
        self.collision_probability = 0

        self.status = "safe"

    def calculate(self):

        # -----------------------
        # Относительное положение
        # -----------------------

        rx = (
            self.object2["x"]
            - self.object1["x"]
        )

        ry = (
            self.object2["y"]
            - self.object1["y"]
        )

        rz = (
            self.object2["z"]
            - self.object1["z"]
        )

        # -----------------------
        # Относительная скорость
        # -----------------------

        rvx = (
            self.object2["vx"]
            - self.object1["vx"]
        )

        rvy = (
            self.object2["vy"]
            - self.object1["vy"]
        )

        rvz = (
            self.object2["vz"]
            - self.object1["vz"]
        )

        velocity_squared = (
            rvx ** 2
            + rvy ** 2
            + rvz ** 2
        )

        # Если объекты движутся
        # с одинаковой скоростью
        if velocity_squared == 0:

            time = 0

        else:

            time = -(
                rx * rvx
                + ry * rvy
                + rz * rvz
            ) / velocity_squared

        # Не смотрим назад во времени
        if time < 0:
            time = 0

        # Не анализируем дальше 24 часов
        if time > self.MAX_TIME:
            time = self.MAX_TIME

        self.closest_time = time

        # -----------------------
        # Расстояние в этот момент
        # -----------------------

        dx = rx + rvx * time
        dy = ry + rvy * time
        dz = rz + rvz * time

        self.minimum_distance = math.sqrt(
            dx ** 2
            + dy ** 2
            + dz ** 2
        )

        self.calculate_probability()

        if (
            self.minimum_distance
            <= self.DANGER_DISTANCE
        ):
            self.status = "dangerous"

        else:
            self.status = "safe"

        return self.minimum_distance

    def calculate_probability(self):

        # Учебная модель оценки риска.
        # Это НЕ реальная физическая
        # вероятность столкновения.

        if (
            self.minimum_distance
            >= self.DANGER_DISTANCE
        ):
            self.collision_probability = 0
            return

        self.collision_probability = (
            1
            - self.minimum_distance
            / self.DANGER_DISTANCE
        )

    def is_dangerous(self):
        return self.status == "dangerous"