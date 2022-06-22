import pytest
from app.export import NotifyClient, ExportFactory


@pytest.mark.unit
@pytest.mark.parametrize(
    ["service_name", "form_data", "expected_client"],
    (
        [
            "notify",
            {
                "api-key": "".join(str(_) for _ in range(100)),
                "template-id": "12345",
                "reply-id": "reply-to-me",
            },
            NotifyClient,
        ],
    ),
)
def test_export_factory_create_clients_correctly(
    service_name, form_data, expected_client
):
    assert (
        ExportFactory.create_exporter(service_name, **form_data).__dict__
        == expected_client(**form_data).__dict__
    )
