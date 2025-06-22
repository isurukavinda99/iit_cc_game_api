from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException

from app.dto.game_schema import GameResponse, GameCreate
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
async def get_all_games(db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    games = GameService.get_games(invoker=claims.get("email"), db=db)
    return games
