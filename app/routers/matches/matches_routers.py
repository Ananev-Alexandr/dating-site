from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db_connection import get_db
from app.enums import SortEnum
from app.routers.matches import crud, schemas
from app.authorization import services

router = APIRouter(tags=["Matches"])


@router.post("/matches/", response_model=schemas.MatchResponse)
async def create_matches(
    match: schemas.MatchCreate,
    db: Session = Depends(get_db),
    authorization=Depends(services.get_current_user),
        ):
    return crud.create_match(db=db, match=match)


@router.get("/matches/")
async def get_all_matches(
    sort: SortEnum,
    db: Session = Depends(get_db),
    authorization=Depends(services.get_current_user),
        ):
    return JSONResponse(
        content=jsonable_encoder(
            {"matches": crud.get_all_matches(db=db, sort=sort)}
        )
    )


@router.delete("/matches/{match_id}")
async def delete_match(
    match_id: int,
    db: Session = Depends(get_db),
    authorization=Depends(services.get_current_user),
        ):
    return crud.delete_match(id=match_id, db=db)
