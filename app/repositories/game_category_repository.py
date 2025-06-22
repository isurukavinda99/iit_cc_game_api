from sqlalchemy.orm import Session
from app.entity.mst_g_category import GameCategory
from typing import Optional, List


class GameCategoryRepository:

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[GameCategory]:
        return db.query(GameCategory).filter(GameCategory.cat_name == name).first()

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[GameCategory]:
        return db.query(GameCategory).filter(GameCategory.id == id).first()

    @staticmethod
    def create_category(db: Session, name: str, created_by: Optional[str] = None) -> GameCategory:
        category = GameCategory(
            cat_name=name,
            active=True,
            created_by=created_by
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_all(db: Session) -> List[GameCategory]:
        return db.query(GameCategory).all()
