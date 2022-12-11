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
    if not tale_in.heroes:
        heroes_list = await create_heroes(tale_in=tale_in)
        for heroes in heroes_list:
            if len(heroes.descriptions):
                tale_in.heroes = heroes
                break
    if not tale_in.structure:
        structures = await create_structures(tale_in=tale_in)
        for structure in structures:
            if len(structure.parts):
                tale_in.structure = structure
                break
    tale_prompt = await cohere.TalePrompt.create(tale_in.log_line)
    if tale_in.heroes:
        tale_prompt.heroes = {0: dict(tale_in.heroes)}
    if tale_in.structure:
        tale_prompt.structures = {0: tale_in.structure.parts}
    response = await tale_prompt.get_tale(
        tale_in.tale_style, structure=0, heroes=0,
        temperature=tale_in.temperature)
    await tale_prompt.close()
    logger.info('Generated tale:\n %s', response)
    tale_in.stories = [schemas.Story(text=text) for text in response]
    return tale_in


@router.post('/heroes', response_model=list[schemas.HeroBase])
async def create_heroes(
    *, tale_in: schemas.TaleCreate,
) -> Any:
    """
    Create new heroes.
    """
    logger.info('Passed tale:%s', tale_in)
    tale_prompt = await cohere.TalePrompt.create(tale_in.log_line)
    response = await tale_prompt.get_heroes(
        'BUN', temperature=tale_in.temperature)
    logger.info('Generated heroes:\n %s', response)
    await tale_prompt.close()
    return [schemas.HeroBase(**hero)
            for hero in response.values() if hero['descriptions']]


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
    response = await tale_prompt.get_structure(
        heroes=0, temperature=tale_in.temperature)
    logger.info('Generated structures:\n %s', response)
    await tale_prompt.close()
    return [schemas.Structure(parts=item) for item in response.values()]
