import argparse
from sqlalchemy.orm import Session
from src.core.database import SessionLocal
from src.core.models import Sender, Event

def list_senders(db: Session):
    senders = db.query(Sender).all()
    print("\n--- Known Senders ---")
    for s in senders:
        print(f"ID: {s.id} | Platform: {s.platform} | Identifier: {s.identifier} | Action: {s.action_rule}")
    print("---------------------\n")

def update_sender(db: Session, sender_id: int, action: str):
    sender = db.query(Sender).filter(Sender.id == sender_id).first()
    if not sender:
        print(f"Sender with ID {sender_id} not found.")
        return
    
    sender.action_rule = action
    db.commit()
    print(f"Updated sender {sender_id} to '{action}'.")

def list_events(db: Session):
    events = db.query(Event).all()
    print("\n--- Saved Calendar Events ---")
    for e in events:
        print(f"ID: {e.id} | Title: '{e.title}' | Location: '{e.location}' | Status: {e.status} | Created: {e.created_at}")
    print("-----------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Assistant Senders and Events")
    parser.add_argument("--list", action="store_true", help="List all senders")
    parser.add_argument("--approve", type=int, metavar="ID", help="Approve a sender ID for auto-sync")
    parser.add_argument("--ignore", type=int, metavar="ID", help="Ignore a sender ID")
    parser.add_argument("--events", action="store_true", help="List all saved events")
    
    args = parser.parse_args()
    db = SessionLocal()
    
    try:
        if args.approve is not None:
            update_sender(db, args.approve, "auto-sync")
        elif args.ignore is not None:
            update_sender(db, args.ignore, "ignore")
        elif args.list:
            list_senders(db)
        elif args.events:
            list_events(db)
        else:
            parser.print_help()
    finally:
        db.close()
