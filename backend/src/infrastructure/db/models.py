import enum

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    ForeignKey, Enum, JSON, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class UserRole(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=True)
    vk_group_id = Column(Integer, nullable=True, index=True)
    vk_api_token = Column(String, nullable=True)
    is_bot_active = Column(Boolean, default=False, nullable=False)
    is_main = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    users = relationship("TenantUser", back_populates="tenant", cascade="all, delete-orphan")
    games = relationship("TenantGame", back_populates="tenant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tenant(id={self.id}, vk_group_id={self.vk_group_id})>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    vk_user_id = Column(Integer, nullable=True, index=True, unique=True)
    is_superadmin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    tenants = relationship("TenantUser", back_populates="user", cascade="all, delete-orphan")
    games = relationship("UserGame", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, vk_user_id={self.vk_user_id})>"


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    rule = Column(Text, nullable=True)  # markdown
    algorithm = Column(JSON, nullable=True)  # jsonb
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    users = relationship("UserGame", back_populates="game", cascade="all, delete-orphan")
    tenants = relationship("TenantGame", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(id={self.id}, name={self.name})>"


class UserGame(Base):
    __tablename__ = "users_games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    balance = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    statistic = Column(JSON, nullable=True)  # jsonb
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="games")
    game = relationship("Game", back_populates="users")

    __table_args__ = (
        UniqueConstraint("user_id", "game_id", name="uq_users_games_user_game"),
        Index("ix_users_games_user_id_game_id", "user_id", "game_id"),
    )

    def __repr__(self):
        return f"<UserGame(user_id={self.user_id}, game_id={self.game_id})>"


class TenantGame(Base):
    __tablename__ = "tenants_games"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    tenant = relationship("Tenant", back_populates="games")
    game = relationship("Game", back_populates="tenants")

    __table_args__ = (
        UniqueConstraint("group_id", "game_id", name="uq_tenants_games_group_game"),
        Index("ix_tenants_games_group_id_game_id", "group_id", "game_id"),
    )

    def __repr__(self):
        return f"<TenantGame(group_id={self.group_id}, game_id={self.game_id})>"


class TenantUser(Base):
    __tablename__ = "tenants_users"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(Text, nullable=True)  # markdown
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Связи
    tenant = relationship("Tenant", back_populates="users")
    user = relationship("User", back_populates="tenants")

    # Уникальность пары (group_id, user_id)
    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="uq_tenants_users_group_user"),
        Index("ix_tenants_users_group_id_user_id", "group_id", "user_id"),
    )

    def __repr__(self):
        return f"<TenantUser(group_id={self.group_id}, user_id={self.user_id}, role={self.role})>"
