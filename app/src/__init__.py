from src.database import metadata, engine

if __name__ == "__main__":
    import asyncio

    async def main():
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    asyncio.run(main())