import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.services import cohere

router = APIRouter()
logger = logging.getLogger('uvicorn')


@router.post('/', response_model=schemas.TaleBase)
async def create_tale(
    *, tale_in: schemas.TaleCreate,
) -> Any:
    """
    Create new tale.
    """
    logger.info('Passed tale:\n %s', tale_in)
    tale_prompt = await cohere.TalePrompt.create(tale_in.log_line)
    tale_prompt.heroes = {0: dict(tale_in.heroes)}
    tale_prompt.structures = {0: tale_in.structure.parts}
    try:
        response = await tale_prompt.get_tale(
            'MARY', structure=0, heroes=0, max_tokens=500)
        await tale_prompt.close()
        logger.info('Generated tale:\n %s', response)
    except cohere.CohereError as error:
        await tale_prompt.close()
        raise HTTPException(status_code=400, detail=str(error)) from error
    return schemas.TaleBase(
        title=tale_in.title,
        log_line=tale_in.log_line,
        heroes=tale_in.heroes,
        structure=tale_in.structure,
        story=response)


@router.post('/heroes', response_model=list[schemas.HeroBase])
async def create_heroes(
    *, tale_in: schemas.TaleCreate,
) -> Any:
    """
    Create new heroes.
    """
    logger.info('Passed tale:%s', tale_in)
    tale_prompt = await cohere.TalePrompt.create(tale_in.log_line)
    try:
        response = await tale_prompt.get_heroes('BUN')
        logger.info('Generated heroes:\n %s', response)
        await tale_prompt.close()
        return [schemas.HeroBase(**hero) for hero in response.values()]
    except cohere.CohereError as error:
        await tale_prompt.close()
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post('/structures', response_model=list[schemas.Structure])
async def create_structures(
    *, tale_in: schemas.TaleCreate,
) -> Any:
    """
    Create new structures.
    """
    logger.info('Passed tale:\n %s', tale_in)
    tale_prompt = await cohere.TalePrompt.create(tale_in.log_line)
    tale_prompt.heroes = {0: dict(tale_in.heroes)}
    try:
        response = await tale_prompt.get_structure(heroes=0, max_tokens=250)
        logger.info('Generated structures:\n %s', response)
        await tale_prompt.close()
        return [schemas.Structure(parts=item) for item in response.values()]
    except cohere.CohereError as error:
        await tale_prompt.close()
        raise HTTPException(status_code=400, detail=str(error)) from error
