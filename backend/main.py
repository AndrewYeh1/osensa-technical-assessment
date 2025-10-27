import random
import sys
import asyncio
import json
from aiomqtt import Client

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# connection variables
BROKER_HOST = "localhost"
BROKER_PORT = 1883
FOOD_TOPIC = "foodOrder"
SERVE_TOPIC = "foodServer"

# serve food callback
async def serve_food(client, json_string, wait):
    await asyncio.sleep(wait)
    print(f"Serving table {json_string.get('table')} with {json_string.get('food')}")
    await client.publish(SERVE_TOPIC, json.dumps(json_string))

# on message callback
def on_message(client, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        json_string = json.loads(payload_str)
        wait = random.randint(1, 10)
        print(f"Received order for {json_string.get('food')} from table {json_string.get('table')}, processing for {wait} seconds")

        task = serve_food(client, json_string, wait)
        asyncio.run_coroutine_threadsafe(task, asyncio.get_event_loop())
    except Exception as e:
        print(f"Error processing message: {e}")

async def main():
    async with Client(BROKER_HOST, BROKER_PORT) as client:
        print("Connected to broker.")
        await client.subscribe(FOOD_TOPIC)
        async for message in client.messages:
            on_message(client, message)

if __name__ == "__main__":
    asyncio.run(main())