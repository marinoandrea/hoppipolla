from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class PolicyModel(BaseModel):
    __tablename__ = "policy"

    issuer_id: Mapped[UUID] = mapped_column(ForeignKey("issuer.id"))
    statements: Mapped[str] = mapped_column(Text())
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean())

    issuer: Mapped["IssuerModel"] = relationship(back_populates="policies")

    def __repr__(self) -> str:
        return f"PolicyModel({self.id=!r})"


class MetaPolicyModel(BaseModel):
    __tablename__ = "meta_policy"

    statements: Mapped[str] = mapped_column(Text())

    def __repr__(self) -> str:
        return f"MetaPolicyModel({self.id=!r})"


class IssuerModel(BaseModel):
    __tablename__ = "issuer"

    name: Mapped[str] = mapped_column(Text(), unique=True)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)

    issuer: Mapped[list["PolicyModel"]] = relationship(
        "PolicyModel", back_populates="issuer")

    def __repr__(self) -> str:
        return f"IssuerModel({self.id=!r}, {self.name=!r})"
