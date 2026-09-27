class Notification:
    def __init__(
        self,
        conjunction_id,
        owner_name,
        message,
        status="created",
        response=None
    ):
        if not owner_name:
            raise ValueError(
                "Не указан владелец спутника"
            )

        if not message:
            raise ValueError(
                "Текст уведомления не может быть пустым"
            )

        self.conjunction_id = conjunction_id
        self.owner_name = owner_name
        self.message = message
        self.status = status
        self.response = response

    def send_notification(self):
        self.status = "sent"

    def register_response(self, response):
        self.response = response