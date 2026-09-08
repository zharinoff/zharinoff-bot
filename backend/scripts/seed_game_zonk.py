import asyncio

from sqlalchemy import select
from src.infrastructure.db.models import Game
from src.infrastructure.db.session import AsyncSessionLocal


async def seed_game_zonk():
    async with AsyncSessionLocal() as session:
        stmt = select(Game).where(Game.name == "Zonk")
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            return

        game = Game(
            name="Zonk",
            description="Игра в кости. Используется 5 костей",
        )

        session.add(game)
        await session.commit()


async def main():
    await seed_game_zonk()


if __name__ == "__main__":
    asyncio.run(main())
