import random
import sys
import asyncio
from aiomqtt import Client

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# connection variables
BROKER_HOST = "localhost"
BROKER_PORT = 1883
FOOD_TOPIC = "foodOrder"
SERVE_TOPIC = "foodServer"

# serve food callback
async def serve_food(client, payload_str, wait):
    print("waiting")
    await asyncio.sleep(wait)
    print("serving")
    await client.publish(SERVE_TOPIC, payload_str)

# on message callback
def on_message(client, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        print(f"Received order on topic '{msg.topic}': {payload_str}")

        task = serve_food(client, payload_str, random.randint(1, 10))
        asyncio.run_coroutine_threadsafe(task, asyncio.get_event_loop())
    except Exception as e:
        print(f"Error processing message: {e}")

async def main():
    async with Client(BROKER_HOST, BROKER_PORT) as client:
        await client.subscribe(FOOD_TOPIC)
        async for message in client.messages:
            on_message(client, message)

if __name__ == "__main__":
    asyncio.run(main())