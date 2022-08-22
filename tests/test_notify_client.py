import pytest

from app.export import NotifyClient
from unittest.mock import Mock


class TestNotifyClient:
    @pytest.mark.unit
    def test_send_email(self):
        client = NotifyClient(
            api_key="".join(str(_) for _ in range(50)),
            **{
                "template-id-field-mentees-matches": "paired-mentees",
                "template-id-field-mentees-no-matches": "solo-mentees",
                "template-id-field-mentors-matches": "paired-mentors",
                "template-id-field-mentors-no-matches": "solo-mentors",
            }
        )

        client.send_email_notification = Mock()
        client.send_email(
            "joebloggs@test.com", **{"type": "csmentor", "number of matches": "0"}
        )
        client.send_email_notification.assert_called_once_with(
            email_address="joebloggs@test.com",
            template_id="solo-mentors",
            personalisation={"type": "csmentor", "number of matches": "0"},
            email_reply_to_id=None,
        )
