import asyncio
from src.core.event_bus import event_bus
from src.core.database import Base, engine
# Import sender_manager to ensure it subscribes
import src.core.sender_manager

# Recreate DB for testing
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

async def run_test():
    # Start the event bus in the background
    bus_task = asyncio.create_task(event_bus.start())
    
    # Wait a bit for bus to start
    await asyncio.sleep(1)
    
    print("Publishing test message from unknown sender...")
    # Simulate a new message from an unknown sender
    await event_bus.publish("new_message", {
        "platform": "telegram",
        "identifier": "@john_doe",
        "text": "Let's meet tomorrow at 10 AM."
    })
    
    # Wait for the event to be processed (should trigger notification and create DB entry)
    await asyncio.sleep(3)
    
    print("Stopping event bus...")
    event_bus.stop()
    await bus_task

if __name__ == "__main__":
    asyncio.run(run_test())
