from typing import TypedDict

from notifications_python_client import NotificationsAPIClient


class ParticipantDict(TypedDict):
    pass


class NotifyClient(NotificationsAPIClient):
    def __init__(self, **kwargs):
        super(NotifyClient, self).__init__(api_key=kwargs.get("api_key"))
        template_prefix = "template-id-field-"
        self.templates: dict[str, str] = {
            key[len(template_prefix) :]: value
            for key, value in kwargs.items()
            if key.startswith(template_prefix)
        }
        self.email_reply_to_id: str = kwargs.get("reply-id", None)

    def send_email(self, recipient: str, **personalisation_data):
        self.send_email_notification(
            email_address=recipient,
            template_id=self._get_template(personalisation_data),
            personalisation=personalisation_data,
            email_reply_to_id=self.email_reply_to_id,
        )

    def _get_template(self, person: dict[str, str]) -> str:
        number_matches = int(person.get("number of matches"))
        person_type = person.get("type")
        if person_type == "csmentor":
            if number_matches > 0:
                return self.templates["mentor-matches"]
            else:
                return self.templates["mentors-no-matches"]
        else:
            if number_matches > 0:
                return self.templates["mentees-matches"]
            else:
                return self.templates["mentees-no-matches"]


class ExportFactory:
    available_services = {"notify": NotifyClient}

    @classmethod
    def create_exporter(cls, service_name: str, **kwargs):
        exporter_class = cls.available_services[service_name]
        return exporter_class(**kwargs)
