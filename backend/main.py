import asyncio
import paho.mqtt.client as mqtt

# connection variables
BROKER_HOST = "localhost"
BROKER_PORT = 1883
FOOD_TOPIC = "foodOrder"
SERVE_TOPIC = "foodServer"

# on connection callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully to {BROKER_HOST}:{BROKER_PORT}")
        # subscribe to the topic upon successful connection
        client.subscribe(FOOD_TOPIC)
        print(f"Subscribed to topic: {FOOD_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

# on message callback
def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        print(f"Received order on topic '{msg.topic}': {payload_str}")

        client.publish(SERVE_TOPIC, payload_str)
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # create client
    client = mqtt.Client(client_id="food_server")
    client.on_connect = on_connect
    client.on_message = on_message

    # start a connection
    try:
        print(f"Attempting to connect to broker at {BROKER_HOST}:{BROKER_PORT}")
        client.connect(BROKER_HOST, BROKER_PORT, 60)
    except ConnectionRefusedError:
        print("Connection failed!")
        exit()
    except Exception as e:
        print(f"An error occurred during connection: {e}")
        exit()

    # keep client connected
    print("Starting MQTT loop, waiting for messages...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()