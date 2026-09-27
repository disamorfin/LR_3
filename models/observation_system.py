class ObservationSystem:
    def __init__(
        self,
        name,
        system_type,
        coverage_area,
        sensitivity,
        status="active"
    ):
        if not name:
            raise ValueError(
                "Название средства наблюдения обязательно"
            )

        if not system_type:
            raise ValueError(
                "Тип средства наблюдения обязателен"
            )

        if sensitivity < 0:
            raise ValueError(
                "Чувствительность не может быть отрицательной"
            )

        self.name = name
        self.system_type = system_type
        self.coverage_area = coverage_area
        self.sensitivity = sensitivity
        self.status = status

    def change_status(self, new_status):
        self.status = new_status

    def schedule_maintenance(self):
        self.status = "maintenance"