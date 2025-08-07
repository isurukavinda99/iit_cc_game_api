from sqlalchemy.orm import Session, joinedload

from app.dto.game_schema import GameUpdate
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


    @staticmethod
    def update_game(invoker: str, game_id: int, update_data: GameUpdate, db: Session):
        game = db.query(GameModal).filter(GameModal.id == game_id).first()

        if not game:
            return None  # This is checked in the service layer

        # Update only the fields provided in update_data
        if update_data.name is not None:
            game.name = update_data.name

        if update_data.category_id is not None:
            game.category_id = update_data.category_id

        if update_data.active is not None:
            game.active = update_data.active

        game.updated_by = invoker

        try:
            db.commit()
            db.refresh(game)
            return game
        except Exception as e:
            db.rollback()
            raise e