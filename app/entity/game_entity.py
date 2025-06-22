from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.config.config import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey("mst_g_category.id"), nullable=False)

    # Relationship
    category = relationship("GameCategory", back_populates="games")

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)