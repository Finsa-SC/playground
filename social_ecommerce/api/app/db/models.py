
import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import (
    CITEXT,
    JSONB,
    UUID,
    ENUM as PGEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


# ============================================================
# ENUMS
# ============================================================


class UserStatus(str, enum.Enum):
    active = "active"
    suspended = "suspended"
    disabled = "disabled"
    pending_verification = "pending_verification"


class ProductStatus(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    suspended = "suspended"
    archived = "archived"


class ModerationAction(str, enum.Enum):
    submitted = "submitted"
    approved = "approved"
    rejected = "rejected"
    suspended = "suspended"
    reinstated = "reinstated"


# ============================================================
# USERS
# ============================================================


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    email: Mapped[str] = mapped_column(
        CITEXT,
        unique=True,
    )

    username: Mapped[str] = mapped_column(
        CITEXT,
        unique=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(100),
    )

    password_hash: Mapped[str | None] = mapped_column(
        Text,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
    )

    avatar_key: Mapped[str | None] = mapped_column(
        Text,
    )

    banner_key: Mapped[str | None] = mapped_column(
        Text,
    )

    status: Mapped[UserStatus] = mapped_column(
        PGEnum(
            UserStatus,
            name="user_status",
            native_enum=True,
            create_type=False,
        ),
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    # Only user_id is used for this relationship.
    # granted_by is a separate FK to users.id.
    roles: Mapped[list["UserRole"]] = relationship(
        back_populates="user",
        foreign_keys="UserRole.user_id",
    )


# ============================================================
# ROLES
# ============================================================


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(30),
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
    )

    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    granted_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    # User who owns this role.
    user: Mapped["User"] = relationship(
        back_populates="roles",
        foreign_keys=[user_id],
    )

    # Role assigned to the user.
    role: Mapped["Role"] = relationship(
        foreign_keys=[role_id],
    )

    # User who granted this role.
    grantor: Mapped["User | None"] = relationship(
        foreign_keys=[granted_by],
    )


# ============================================================
# AUTHENTICATION
# ============================================================


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


# ============================================================
# CATALOG
# ============================================================


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
    )

    slug: Mapped[str] = mapped_column(
        CITEXT,
        unique=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    seller_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
    )

    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("categories.id"),
    )

    title: Mapped[str] = mapped_column(
        String(200),
    )

    description: Mapped[str] = mapped_column(
        Text,
    )

    price: Mapped[object] = mapped_column(
        Numeric(18, 2),
    )

    currency: Mapped[str] = mapped_column(
        String(3),
    )

    stock_quantity: Mapped[int] = mapped_column(
        Integer,
    )

    status: Mapped[ProductStatus] = mapped_column(
        PGEnum(
            ProductStatus,
            name="product_status",
            native_enum=True,
            create_type=False,
        ),
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


# ============================================================
# PRODUCT MODERATION
# ============================================================


class ProductModerationEvent(Base):
    __tablename__ = "product_moderation_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id"),
    )

    moderator_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    action: Mapped[ModerationAction] = mapped_column(
        PGEnum(
            ModerationAction,
            name="moderation_action",
            native_enum=True,
            create_type=False,
        ),
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
    )

    metadata_: Mapped[dict] = mapped_column(
        "metadata",
        JSONB,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
