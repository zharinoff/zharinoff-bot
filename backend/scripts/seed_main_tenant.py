import asyncio

from settings import settings
from sqlalchemy import select
from src.infrastructure.db.models import Tenant
from src.infrastructure.db.session import AsyncSessionLocal
from src.infrastructure.secrets.token_encryptor import encryptor


async def seed_main_tenant() -> None:
    async with AsyncSessionLocal() as session:
        stmt = select(Tenant).where(Tenant.is_main == True)
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            return

        token = encryptor.encrypt(settings.vk.TOKEN)

        tenant = Tenant(
            description="Главная группа Бота",
            vk_group_id=settings.vk.GROUP_ID,
            vk_api_token=token,
            is_bot_active=True,
            is_main=True,
        )

        session.add(tenant)
        await session.commit()


async def main() -> None:
    await seed_main_tenant()


if __name__ == "__main__":
    asyncio.run(main())
