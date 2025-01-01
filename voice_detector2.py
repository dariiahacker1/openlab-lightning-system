import paho.mqtt.client as mqtt
import json
import time


broker_host = "openlab.kpi.fei.tuke.sk"
broker_port = 8883
use_secure_connection = True

sensor_topics = [
    "openlab/sensorkits/B8:27:EB:78:8F:4D/vol",
    "openlab/sensorkits/B8:27:EB:DA:2E:65/vol",
    "openlab/sensorkits/B8:27:EB:DC:E8:38/vol",
    "openlab/sensorkits/B8:27:EB:2F:7B:7D/vol",
]

output_topic = "openlab/unifiedMapPositions/output"

def publish_output_message(client, message):
    client.publish(output_topic, json.dumps(message))

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
    for topic in sensor_topics:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    try:
        
        data = json.loads(msg.payload)
        process_audio_data(data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Received payload: {msg.payload}")


def process_audio_data(data):
    try:
        if isinstance(data, int):
            volume_level = data
        else:
            volume_level = data.get("value")

        if volume_level is not None:
            timestamp = int(time.time())
            #timestamp = time()
           
            output_message = {
                "Id": "dummy_id",
                "VolumeLevel": volume_level,
                "Timestamp": timestamp,
            }

            publish_output_message(mqtt_client, output_message)
            with open("volume_data.json", "w") as file:
                file.write(json.dumps(output_message) + "\n")
        else:
            print("Error: Sound volume data not found in the expected format.")
    except Exception as e:
        print(f"Error processing audio data: {e}")
        print(f"Received data: {data}")

mqtt_client = mqtt.Client()


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


if use_secure_connection:
    mqtt_client.tls_set()
mqtt_client.connect(broker_host, broker_port, 60)


mqtt_client.loop_start()




while True:
    pass