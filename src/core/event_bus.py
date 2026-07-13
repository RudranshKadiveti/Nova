import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.queue = asyncio.Queue()
        self.running = False

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data: dict):
        await self.queue.put({"type": event_type, "data": data})

    async def start(self):
        self.running = True
        logger.info("Event Bus started.")
        while self.running:
            event = await self.queue.get()
            event_type = event["type"]
            data = event["data"]
            
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(data)
                        else:
                            callback(data)
                    except Exception as e:
                        logger.error(f"Error processing event {event_type}: {e}")
            self.queue.task_done()

    def stop(self):
        self.running = False

event_bus = EventBus()
