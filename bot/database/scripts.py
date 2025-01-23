from sqlalchemy import create_engine
from schemas import Base, BookingSchema
from bot.database.database import engine
import argparse

def do_with_tables(action: str):
    try:
        if action == "recreate":
            # Drop all existing tables
            Base.metadata.drop_all(bind=engine)
            # Create all tables defined in the schemas
            Base.metadata.create_all(bind=engine)
            print("Tables recreated successfully!")
        elif action == "create":
            # Create all tables defined in the schemas
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully!")
        elif action == "drop":
            # Drop all existing tables
            Base.metadata.drop_all(bind=engine)
            print("Tables dropped successfully!")
    except Exception as e:
        print(f"Error managing tables: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage database tables')
    parser.add_argument('--create', action='store_true', help='Create all tables')
    parser.add_argument('--recreate', action='store_true', help='Drop all tables and create them again')
    parser.add_argument('--drop', action='store_true', help='Drop all tables')
    
    args = parser.parse_args()
    
    if args.create:
        do_with_tables("create")
    elif args.drop:
        do_with_tables("drop")
    else:
        # Default behavior: recreate tables
        do_with_tables("recreate")
    
    
