from starlette import status

from app.dto.game_schema import GameCreate
from app.config.config import get_db
from app.exceptions.exceptions import AppExceptionCase
from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.game_repository import GameRepository
from app.repositories.game_category_repository import GameCategoryRepository

class GameService:

    @staticmethod
    def create_game(game: GameCreate, invoker: str, db: Session = Depends(get_db)):

        category = GameCategoryRepository.get_by_id(db, game.category_id)
        if not category:
            raise AppExceptionCase(
                "Category not found",
                status.HTTP_404_NOT_FOUND,
                code="NOT_FOUND"
            )

        try:
            game_data = game.dict()
            game_data["created_by"] = invoker
            game_data["category_id"] = category.id
            return GameRepository.create_game(db, game_data)  # pass dict here
        except Exception as e:
            raise AppExceptionCase(
                "Game creation failed due to DB error : " + str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                code="DB_ERROR"
            ) from e