from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dto.game_schema import GameResponse, GameCreate, GameUpdate
from app.services.game_service import GameService
from app.config.config import get_db
from app.middleware.alb_auth import require_auth
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/game", tags=["games"])

@router.post("", response_model=GameResponse)
async def create_item(item: GameCreate, db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    game = GameService.create_game(game=item, invoker=claims.get("email"), db=db)
    return game

@router.get("")
async def get_all_games( db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    games = GameService.get_games(invoker=claims.get("email"), db=db)
    return games

@router.get("/{game_id}")
async def get_by_id(game_id: int, db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    game = GameService.get_by_id(invoker=claims.get("email"), game_id= game_id, db=db)
    return game

@router.put("/{game_id}")
async def update_game(game_id: int, update_data: GameUpdate, db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    updated_game = GameService.update_game(invoker=claims.get("email"), game_id=game_id, update_data=update_data, db=db)
    return updated_game