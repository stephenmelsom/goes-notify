import random
import time
from pathlib import Path

import click
from loguru import logger

from goes_notifier.app import find_appointments
from goes_notifier.notifiers import DesktopNotifier, EmailNotifier, SMSNotifier
from goes_notifier.util import load_config


@click.command()
@click.option(
    "--config",
    default="./config.toml",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--frequency", type=click.FloatRange(min=0), default=2)
@click.option("--add-jitter", default=True)
@click.option("--enable-sms-notifications", default=False)
@click.option("--enable-email-notifications", default=False)
@click.option("--enable-desktop-notifications", default=False)
def run_server(
    config: Path,
    frequency: float,
    add_jitter: bool,
    enable_sms_notifications: bool,
    enable_email_notifications: bool,
    enable_desktop_notifications: bool,
):
    c = load_config(config)

    notifiers = []
    if enable_sms_notifications:
        notifiers.append(SMSNotifier(**c["sms"]))
    if enable_email_notifications:
        notifiers.append(EmailNotifier(**c["email"]))
    if enable_desktop_notifications:
        notifiers.append(DesktopNotifier())

    jitter_func = random.random if add_jitter else lambda: 0

    while True:
        find_appointments(c["location_codes"], notifiers)
        sleep_time = frequency + jitter_func()
        time.sleep(sleep_time)
        logger.debug(f"Sleeping for {sleep_time:.2f} seconds")


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    run_server()
