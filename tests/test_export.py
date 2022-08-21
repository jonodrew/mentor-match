import pytest
from app.export import NotifyClient, ExportFactory


@pytest.mark.unit
@pytest.mark.parametrize(
    ["service_name", "form_data", "expected_client"],
    (
        [
            "notify",
            {
                "api_key": "".join(str(_) for _ in range(100)),
            },
            NotifyClient,
        ],
    ),
)
def test_export_factory_create_clients_correctly(
    service_name, form_data, expected_client
):
    assert (
        type(ExportFactory.create_exporter(service_name, **form_data))
        == expected_client
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ["client", "form_data", "attributes"],
    [
        (
            "notify",
            {
                "api_key": "".join(str(_) for _ in range(100)),
                "template-id-field-mentees-matches": "paired-mentees",
                "template-id-field-mentees-no-matches": "solo-mentees",
                "template-id-field-mentors-matches": "paired-mentors",
                "template-id-field-mentors-no-matches": "solo-mentors",
                "reply-id": "reply-to-me",
            },
            {
                "api_key": "".join(str(_) for _ in range(100))[-36:],
                "templates": {
                    "mentees-matches": "paired-mentees",
                    "mentees-no-matches": "solo-mentees",
                    "mentors-matches": "paired-mentors",
                    "mentors-no-matches": "solo-mentors",
                },
                "email_reply_to_id": "reply-to-me",
            },
        )
    ],
)
def test_client_has_correct_attributes(client, form_data, attributes):
    c = ExportFactory.create_exporter(client, **form_data)
    for key, value in attributes.items():
        assert getattr(c, key) == value
