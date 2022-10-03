import logging
from prometheus_client import start_http_server, Gauge, Info
from pyEarnapp import EarnApp
from os import environ
from time import sleep
import sys

EARNAPP_TOKEN = environ.get("EARNAPP_TOKEN")
SLEEP_TIME = int(environ.get("SLEEP_TIME", 60))
PORT = int(environ.get("PORT", 8000))

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ])
log = logging.getLogger('server')

def main():
    start_http_server(PORT)
    earnApp = EarnApp(EARNAPP_TOKEN)

    earnapp_balance = Gauge("earnapp_balance", "Current earned balance")
    earnapp_earnings_total = Gauge("earnapp_earnings_total", "Amount earned till date")
    earnapp_multiplier = Gauge("earnapp_multiplier", "Earning multiplier")
    earnapp_bonuses = Gauge("earnapp_bonuses", "Earnings from referrals")
    earnapp_bonuses_total = Gauge(
        "earnapp_bonuses_total", "Total earnings from referrals till date"
    )
    earnapp_referral_part = Gauge("earnapp_referral_part", "Referral bonus percentage")

    earnapp_total_bandwidth_usage = Gauge(
        "earnapp_total_bandwidth_usage", "Shows bandwidth usage of all devices combined"
    )
    earnapp_device_bandwidth_usage = Gauge(
        "earnapp_device_bandwidth_usage", "Unredeemed bandwidth usage", ["uuid"]
    )
    earnapp_device_total_bandwidth_usage = Gauge(
        "earnapp_device_total_bandwidth_usage", "Total bandwindth usage", ["uuid"]
    )
    earnapp_device_redeemed_bandwidth = Gauge(
        "earnapp_device_redeemed_bandwidth", "Redeemed bandwidth usage", ["uuid"]
    )
    earnapp_device_rate = Gauge(
        "earnapp_device_rate", "Price/GB of the device", ["uuid"]
    )
    earnapp_device_info = Info("earnapp_device", "Device Info", ["uuid"])

    while True:
        try:
            infos = earnApp.get_earning_info()
            devices_infos = earnApp.get_devices_info()

            earnapp_balance.set(infos.balance)
            earnapp_earnings_total.set(infos.earnings_total)
            earnapp_multiplier.set(infos.multiplier)
            earnapp_bonuses.set(infos.bonuses)
            earnapp_bonuses_total.set(infos.bonuses_total)
            earnapp_referral_part.set(int(infos.referral_part.replace("%", "")) / 100)
            earnapp_total_bandwidth_usage.set(devices_infos.total_bandwidth_usage)
            for device in devices_infos.devices:
                earnapp_device_bandwidth_usage.labels(device.uuid).set(
                    device.bandwidth_usage
                )
                earnapp_device_total_bandwidth_usage.labels(device.uuid).set(
                    device.total_bandwidth_usage
                )
                earnapp_device_redeemed_bandwidth.labels(device.uuid).set(
                    device.redeemed_bandwidth
                )
                earnapp_device_rate.labels(device.uuid).set(device.rate)
                earnapp_device_info.labels(device.uuid).info(
                    {"country": device.country, "device_type": device.device_type}
                )
        except KeyboardInterrupt as exc:
            raise exc
        except Exception as exc:
            log.error(exc)
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Shutting down ...")
        exit(0)
