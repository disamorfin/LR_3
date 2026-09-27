class Observation:
    def __init__(
        self,
        space_object_id,
        observation_system_id,
        date_time,
        orbital_data
    ):
        self.space_object_id = space_object_id
        self.observation_system_id = observation_system_id
        self.date_time = date_time
        self.orbital_data = orbital_data

    def validate_data(self):
        if self.space_object_id <= 0:
            raise ValueError(
                "Некорректный ID космического объекта"
            )

        if self.observation_system_id <= 0:
            raise ValueError(
                "Некорректный ID средства наблюдения"
            )

        if not self.date_time:
            raise ValueError(
                "Не указана дата наблюдения"
            )

        return True

    def save_observation(self):
        return True