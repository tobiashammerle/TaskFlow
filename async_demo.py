import asyncio
import time


async def load_tasks(name, seconds):
    print(f"{name}: Laden gestartet")
    time.sleep(seconds)
    print(f"{name}: Laden beendet")


async def main():
    await asyncio.gather(load_tasks("Task 1", 3), load_tasks("Task 2", 1))


asyncio.run(main())
