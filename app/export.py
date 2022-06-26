from notifications_python_client import NotificationsAPIClient


class NotifyClient(NotificationsAPIClient):
    def __init__(self, **kwargs):
        super(NotifyClient, self).__init__(kwargs.get("api-key"))
        self.template_id: str = kwargs.get("template-id")
        self.email_reply_to_id: str = kwargs.get("reply-id")

    def send_email(self, recipient: str, **personalisation_data):
        self.send_email_notification(
            email_address=recipient,
            template_id=self.template_id,
            personalisation=personalisation_data,
            email_reply_to_id=self.email_reply_to_id,
        )


class ExportFactory:
    available_services = {"notify": NotifyClient}

    @classmethod
    def create_exporter(cls, service_name: str, **kwargs):
        exporter_class = cls.available_services[service_name]
        return exporter_class(**kwargs)
