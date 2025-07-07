from sqlalchemy.orm import Session, joinedload
from app.entity.game_entity import Game as GameModal

class GameRepository:
    @staticmethod
    def create_game(db: Session, game_data: dict):
        try:
            db_item = GameModal(**game_data)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_all(db: Session):
        return db.query(GameModal).options(joinedload(GameModal.category)).all()

    @staticmethod
    def get_by_id(game_id: int, db: Session):
        return db.query(GameModal).options(joinedload(GameModal.category)).filter(GameModal.id == game_id).first()