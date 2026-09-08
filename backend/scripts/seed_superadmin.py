import asyncio

from settings import settings
from sqlalchemy import select
from src.infrastructure.db.models import User
from src.infrastructure.db.session import AsyncSessionLocal


async def seed_superadmin():
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.is_superadmin == True)
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            return

        user = User(
            vk_user_id=settings.vk.ADMIN_ID,
            is_superadmin=True,
        )

        session.add(user)
        await session.commit()


async def main():
    await seed_superadmin()


if __name__ == "__main__":
    asyncio.run(main())
