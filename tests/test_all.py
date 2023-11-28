import json
from pathlib import Path

import pytest
from goes_notifier.notifiers import DesktopNotifier, EmailNotifier, SMSNotifier

from goes_notifier.util import Appointment, load_config

TEST_CONFIG = "config-test.toml"
NO_TEST_CONFIG = not Path(TEST_CONFIG).exists()


@pytest.fixture
def response():
    return """{
            "locationId" : 5001,
            "startTimestamp" : "2023-11-28T08:25",
            "endTimestamp" : "2023-11-28T08:35",
            "active" : true,
            "duration" : 10,
            "remoteInd" : false
        }"""


@pytest.fixture
def config():
    return load_config(TEST_CONFIG)


@pytest.fixture
# pylint: disable=redefined-outer-name
def appointment(response: str):
    return Appointment(**json.loads(response))


# pylint: disable=redefined-outer-name
def test_parse_response(response: str):
    d = json.loads(response)
    Appointment(**d)


@pytest.mark.skipif(NO_TEST_CONFIG, reason="Test config file not found.")
def test_notify_email(config: dict, appointment: Appointment):
    notifier = EmailNotifier(**config["email"])
    notifier.notify(appointments=[appointment])


@pytest.mark.skipif(NO_TEST_CONFIG, reason="Test config file not found.")
def test_notify_sms(config: dict, appointment: Appointment):
    notifier = SMSNotifier(**config["sms"])
    notifier.notify(appointments=[appointment])


def test_notify_desktop(appointment: Appointment):
    notifier = DesktopNotifier()
    notifier.notify(appointments=[appointment])


d = json.loads("""{
            "locationId" : 5001,
            "startTimestamp" : "2023-11-28T08:25",
            "endTimestamp" : "2023-11-28T08:35",
            "active" : true,
            "duration" : 10,
            "remoteInd" : false
        }""")
a = Appointment(**d)
print(a)
test_notify_desktop(a)
