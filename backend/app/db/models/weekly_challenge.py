from sqlalchemy import (
    Column, BigInteger, Boolean, DateTime, Enum, ForeignKey, CheckConstraint,
    Index, func, Text, String, Integer
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

# from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, UniqueConstraint, Index, func
# from sqlalchemy.orm import relationship
# from app.core.database import Base
# from app.db.models.weekly_challenge import WeeklyChallenge

class EntityKind(str, enum.Enum):
    ASSET = "ASSET"
    TYPE = "TYPE"
    REGION = "REGION"

class InstrumentType(str, enum.Enum):
    STOCK = "Action"
    ETF = "ETF"
    CRYPTO = "Crypto"

class Region(str, enum.Enum):
    AFRICA = "Afrique"
    USA = "États-Unis"
    EUROPE = "Europe"
    WORLD = "Monde"

class WeeklyChallenge(Base):
    __tablename__ = "weekly_challenges"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at   = Column(DateTime(timezone=True), nullable=False)
    selection_end_at   = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="false")

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    description = Column(Text, nullable=True)
    
    # 👇 NEW column
    winning_side_id = Column(
        BigInteger,
        ForeignKey("weekly_challenge_sides.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Optional: relationship for convenience
    # ✅ Must specify foreign_keys
    winning_side = relationship(
        "WeeklyChallengeSide",
        foreign_keys=[winning_side_id]
    )

    # ✅ Must specify foreign_keys
    sides = relationship(
        "WeeklyChallengeSide",
        back_populates="challenge",
        cascade="all, delete-orphan",
        foreign_keys="WeeklyChallengeSide.challenge_id"
    )

    picks = relationship(
        "WeeklyChallengePick",
        back_populates="challenge",
        cascade="all, delete-orphan"
    )
    
    # winning_side = relationship("WeeklyChallengeSide", foreign_keys=[winning_side_id])  
    # sides = relationship("WeeklyChallengeSide", back_populates="challenge", cascade="all, delete-orphan")
    # picks = relationship("WeeklyChallengePick", back_populates="challenge", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("end_at > start_at", name="ck_weekly_challenges_valid_window"),
        Index("ix_weekly_challenges_active", "is_active"),
        Index("ix_weekly_challenges_window", "start_at", "end_at"),
    )

class WeeklyChallengeSide(Base):
    __tablename__ = "weekly_challenge_sides"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    challenge_id = Column(BigInteger, ForeignKey("weekly_challenges.id", ondelete="CASCADE"), nullable=False)

    # Use 'A' or 'B'
    side = Column(String(1), nullable=False)  # 'A' or 'B'

    # What this side represents
    entity_kind = Column(Enum(EntityKind, name="challenge_entity_kind"), nullable=False)

    # If ASSET
    asset_id = Column(BigInteger, ForeignKey("assets.id", ondelete="RESTRICT"), nullable=True)

    # If TYPE (instrument category)
    instrument_type = Column(Enum(InstrumentType, name="challenge_instrument_type"), nullable=True)

    # If REGION
    region = Column(Enum(Region, name="challenge_region"), nullable=True)

    # challenge = relationship("WeeklyChallenge", back_populates="sides")
    # asset = relationship("Asset")

    challenge = relationship(
        "WeeklyChallenge",
        back_populates="sides",
        foreign_keys=[challenge_id]
    )

    asset = relationship("Asset")
    
    __table_args__ = (
        # Only one row per side per challenge
        Index("uq_weekly_challenge_side_unique", "challenge_id", "side", unique=True),

        # Exactly one discriminator is populated depending on entity_kind
        CheckConstraint(
            "(entity_kind = 'ASSET'  AND asset_id IS NOT NULL AND instrument_type IS NULL AND region IS NULL) OR "
            "(entity_kind = 'TYPE'   AND asset_id IS NULL     AND instrument_type IS NOT NULL AND region IS NULL) OR "
            "(entity_kind = 'REGION' AND asset_id IS NULL     AND instrument_type IS NULL     AND region IS NOT NULL)",
            name="ck_weekly_challenge_sides_kind_fields"
        ),

        # Side must be 'A' or 'B'
        CheckConstraint("side IN ('A','B')", name="ck_weekly_challenge_sides_side_ab"),
    )




class WeeklyChallengePick(Base):
    __tablename__ = "weekly_challenge_picks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    challenge_id = Column(BigInteger, ForeignKey("weekly_challenges.id", ondelete="CASCADE"), nullable=False)
    user_id      = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # The chosen side (refer to sides table)
    side_id      = Column(BigInteger, ForeignKey("weekly_challenge_sides.id", ondelete="RESTRICT"), nullable=False)
    result       = Column(Boolean,  nullable=False)
    created_at   = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    
    challenge = relationship("WeeklyChallenge", back_populates="picks")
    user      = relationship("User")
    side      = relationship("WeeklyChallengeSide")

    __table_args__ = (
        # One pick per user per challenge
        Index("uq_weekly_challenge_pick_once", "challenge_id", "user_id", unique=True),
        Index("ix_weekly_challenge_picks_challenge", "challenge_id"),
        Index("ix_weekly_challenge_picks_user", "user_id"),
    )

