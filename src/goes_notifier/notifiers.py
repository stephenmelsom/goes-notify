import subprocess

import yagmail
from jinja2 import Environment, PackageLoader, select_autoescape
from twilio.rest import Client

from goes_notifier.util import Appointment

env = Environment(loader=PackageLoader("goes_notifier"), autoescape=select_autoescape())


class Notifier:
    def notify(self, appointments: list[Appointment]) -> None:
        raise NotImplementedError


class EmailNotifier(Notifier):
    subject: str = "Alert: Global Entry interview openings are available"

    def __init__(self, user: str, oauth_file: str, recipients: list[str]):
        self.yag = yagmail.SMTP(user, oauth2_file=oauth_file)
        self.recipients = recipients
        self.template = env.get_template("email.jinja2")

    def notify(self, appointments: list[Appointment]):
        message = self.template.render(appointments=appointments)
        self.yag.send(self.recipients, self.subject, message)


class SMSNotifier(Notifier):
    def __init__(
        self,
        twilio_account_sid: str,
        twilio_auth_token: str,
        from_number: str,
        to_number: str,
    ):
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.from_number = from_number
        self.to_number = to_number

    def notify(self, appointments: list[Appointment]):
        body = "New GOES appointment available!"
        self.client.messages.create(
            body=body, to=self.to_number, from_=self.from_number
        )


class DesktopNotifier(Notifier):
    def notify(self, appointments: list[Appointment]):
        message = f"Found {len(appointments)} new appointment(s)!"
        command = f'display notification "{message}" with title "Global Entry Notifier" sound name "Ping"'
        subprocess.run(["osascript", "-e", command], check=True)
