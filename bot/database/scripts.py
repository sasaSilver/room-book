from bot.database.core import engine
from bot.database.schemas import Base

async def do_with_tables(action: str):
    async with engine.begin() as conn:
        if action == "recreate":
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        elif action == "create":
            await conn.run_sync(Base.metadata.create_all)
        elif action == "drop":
            await conn.run_sync(Base.metadata.drop_all)

if __name__ == "__main__":
    import argparse, asyncio
    parser = argparse.ArgumentParser(description='Manage database tables')
    parser.add_argument('--create', action='store_true', help='Create all tables')
    parser.add_argument('--recreate', action='store_true', help='Drop all tables and create them again')
    parser.add_argument('--drop', action='store_true', help='Drop all tables')
    
    args = parser.parse_args()
    
    if args.create:
        asyncio.run(do_with_tables("create"))
    elif args.recreate:
        asyncio.run(do_with_tables("recreate"))
    elif args.drop:
        asyncio.run(do_with_tables("drop"))
    else:
        parser.print_help()
