class SpaceObject:
    def __init__(
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
        vz,
        status="active"
    ):
        if not catalog_number:
            raise ValueError(
                "Каталожный номер не может быть пустым"
            )

        if not object_type:
            raise ValueError(
                "Тип объекта не может быть пустым"
            )

        if size < 0:
            raise ValueError(
                "Размер объекта не может быть отрицательным"
            )

        self.catalog_number = catalog_number
        self.international_id = international_id
        self.object_type = object_type
        self.size = size

        self.x = x
        self.y = y
        self.z = z

        self.vx = vx
        self.vy = vy
        self.vz = vz

        self.status = status

    def update_status(self, new_status):
        self.status = new_status

    def mark_as_lost(self):
        self.status = "lost"

    def mark_as_found(self):
        self.status = "active"