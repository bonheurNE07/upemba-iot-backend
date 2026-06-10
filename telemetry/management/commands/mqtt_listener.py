import json
import logging

import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand

from inventory.models import Equipment
from telemetry.models import SensorReading

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Starts a long-running process that listens to the Mosquitto MQTT broker for ESP32 telemetry."

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.stdout.write(self.style.SUCCESS("Connected to Mosquitto MQTT Broker!"))
            topic = getattr(settings, "MQTT_TELEMETRY_TOPIC", "upemba/telemetry")
            client.subscribe(topic)
            self.stdout.write(f"Subscribed to topic: {topic}")
        else:
            self.stderr.write(self.style.ERROR(f"Failed to connect, return code {rc}"))

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            data = json.loads(payload)
            device_id = data.get("device_id")
            telemetry = data.get("data", {})

            temp = telemetry.get("temp")
            volt = telemetry.get("volt")
            vib = telemetry.get("vib", {})
            vib_x = vib.get("x")
            vib_y = vib.get("y")
            vib_z = vib.get("z")

            if None in (device_id, temp, volt, vib_x, vib_y, vib_z):
                logger.warning(f"Incomplete payload missing keys: {payload}")
                return

            equipment, _ = Equipment.objects.get_or_create(
                mac_address=device_id,
                defaults={
                    "name": f"Sensor Node {device_id}",
                    "equipment_type": Equipment.Type.INVERTER,
                },
            )

            SensorReading.objects.create(
                equipment=equipment,
                temperature=temp,
                voltage=volt,
                vib_x=vib_x,
                vib_y=vib_y,
                vib_z=vib_z,
            )
            # Use basic print since the command loops forever natively
            self.stdout.write(
                self.style.SUCCESS(
                    f"Saved reading for {device_id}: Temp {temp}, Volt {volt}",
                ),
            )

        except json.JSONDecodeError:
            logger.exception(f"Malformed JSON payload: {payload}")
        except Exception as e:
            logger.exception(f"Error processing MQTT message: {e}")

    def handle(self, *args, **options):
        # paho-mqtt v2 usage
        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="django_mqtt_listener",
        )
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        # Settings Configuration
        broker_host = getattr(settings, "MQTT_BROKER_HOST", "mosquitto")
        broker_port = getattr(settings, "MQTT_BROKER_PORT", 1883)
        broker_user = getattr(settings, "MQTT_BROKER_USER", None)
        broker_pass = getattr(settings, "MQTT_BROKER_PASSWORD", None)

        if broker_user and broker_pass:
            client.username_pw_set(broker_user, broker_pass)

        self.stdout.write(f"Connecting to broker {broker_host}:{broker_port}...")

        try:
            client.connect(broker_host, broker_port, 60)
            client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("MQTT Listener stopped by user."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error connecting to MQTT Broker: {e}"))
