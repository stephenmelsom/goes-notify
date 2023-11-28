import requests
from loguru import logger

from goes_notifier.notifiers import Notifier
from goes_notifier.util import Appointment


def _get_interview_dates(timeout: int = 2) -> list[Appointment]:
    url = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest"

    r = requests.get(url, timeout=timeout)

    if r.status_code == 200:
        if data := r.json():
            return [Appointment(**r) for r in data]
    else:
        logger.error(f"Non 200 response code encountered: {r.status_code}")

    return []


class AppointmentObserver:
    notifiers: list[Notifier]

    def __init__(self, notifiers: list[Notifier]) -> None:
        self.notifiers = notifiers

    def notify_new_appointments(self, appointments: list[Appointment]):
        for notifier in self.notifiers:
            notifier.notify(appointments)


# pylint: disable=dangerous-default-value
def find_appointments(location_codes: list[int], notifiers: list[Notifier] = []):
    appt_observer = AppointmentObserver(notifiers)
    appts = _get_interview_dates()
    filtered_appts = list(filter(lambda a: a.locationId in location_codes, appts))
    logger.info(
        f"{len(filtered_appts)}/{len(appts)} available appointments meet the specified criteria"
    )
    appt_observer.notify_new_appointments(filtered_appts)
