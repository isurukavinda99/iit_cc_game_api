from app.config.config import Base
from sqlalchemy import  Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class GameCategory(Base):
    __tablename__ = "mst_g_category"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    cat_name = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, default=True)

    # One-to-many relationship
    games = relationship("Game", back_populates="category", cascade="all, delete-orphan")