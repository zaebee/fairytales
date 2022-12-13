"""Implements tales generator on Cohere service."""

import logging
import re
import os
import cohere
import pandas as pd
from fastapi import HTTPException

from app.services import tales as base_tales

COHERE_KEY = 'onk1aMdIZZ4P86E99JlD095UEVH7LfIUwwmEF7KQ'

# Paste your API key here. Remember to not share it publicly
os.environ['COHERE_KEY'] = COHERE_KEY
logger = logging.getLogger('uvicorn')


class TalePrompt:
    """Generates prompts for tale structure and text."""

    HEAD = ('Examples of breakdowns of story into Vladimir Propp\'s '
            '"Morphology of a fairy tale" structutre.\n')

    SAMPLE = 'Example {counter}.\n{text}\n\n<scenes>\n{predict}\n\n<end>\n'
    SAMPLE_PREDICT = 'Example {counter}. \n{text}\n\n<scenes>'

    HEROES = ('Example {counter}.\n{text}\nCharacters and descriptions:'
              '\n{heroes}\n<end>')
    HEROES_PREDICT = 'Example {counter}.\n{text}\nCharacters and descriptions:'

    def __init__(self, line, as_tale=None, **kwargs):
        _tales = [tale for tale in base_tales.TALES if tale['name'] != 'BUN']
        self.client = None
        self.heroes = {}
        self.structures = {}
        self.line = line
        self.as_tale = as_tale
        self.tales = kwargs.get('tales', _tales)

    async def close(self):
        """Closes connection."""
        await self.client.close_connection()

    @classmethod
    async def create(cls, line, as_tale: str = None, **kwargs):
        """Initializes async client."""
        self = cls(line, as_tale, **kwargs)
        self.client = await cohere.AsyncClient.create(COHERE_KEY)
        return self

    async def generate(
        self, prompt: str, model: str = 'xlarge',
        stop_sequences: list[str] = None, **kwargs
    ) -> str:
        """Generates sequence from given prompt."""
        max_tokens = kwargs.get('max_tokens', 500)
        params = {
            'return_likelihoods': 'GENERATION',
            'stop_sequences': stop_sequences or ['<end>'],
            'num_generations': kwargs.get('num_generations', 3),
            'temperature': kwargs.get('temperature', 0.555),
            'max_tokens': min([max_tokens, max(200, 8788 - len(prompt))])
        }
        logger.info('TALES:%s', [tale['name'] for tale in self.tales])
        logger.info(
            'GENERATING for len(prompt)=%s PARAMS:=%s\n', len(prompt), params)
        try:
            prediction = await self.client.generate(
                model=model, prompt=prompt, **params)
        except cohere.CohereError as error:
            await self.close()
            raise HTTPException(status_code=400, detail=str(error)) from error
        gens = []
        likelihoods = []
        for gen in prediction.generations:
            gens.append(gen.text)

            sum_likelihood = 0
            for token in gen.token_likelihoods:
                sum_likelihood += token.likelihood
            likelihoods.append(sum_likelihood)

        data = pd.DataFrame({'generation': gens, 'likelihood': likelihoods})
        data = data.drop_duplicates(subset=['generation'])
        data = data.sort_values('likelihood', ascending=False, ignore_index=True)
        return data

    def prompt_structure(self, text) -> str:
        """Generates prompt to get tale structure."""
        output = [self.HEAD]
        for counter, tale in enumerate(self.tales, 1):
            sample = self.SAMPLE.format(
                counter=counter, text=tale['summary'], predict=tale['struct'])
            output.append(sample)
        predict = self.SAMPLE_PREDICT.format(
            counter=len(self.tales) + 1, text=text)
        output.append(predict)
        return '\n'.join(output)

    def prompt_text_as_tale(self, text, as_tale) -> str:
        """Generates prompt to get tale full text."""
        tales = [tale for tale in self.tales if tale['name'] == as_tale]
        output = [self.HEAD]
        if not tales:
            return ''
        for counter, tale in enumerate(tales, 1):
            summary = '\n'.join([tale['summary'], tale['struct']])
            sample = self.SAMPLE.format(
                counter=counter, text=summary, predict=tale['text'])
            output.append(sample)
        predict = self.SAMPLE_PREDICT.format(counter=len(tales) + 1, text=text)
        output.append(predict)
        return '\n'.join(output)

    def prompt_structure_as_tale(self, text, as_tale) -> str:
        """Generates prompt to predict tale structure similar as given tale."""
        tales = [tale for tale in self.tales if tale['name'] == as_tale]
        output = [self.HEAD]
        if not tales:
            return ''
        for counter, tale in enumerate(tales, 1):
            sample = self.SAMPLE.format(
                counter=counter, text=tale['text'], predict=tale['struct'])
            output.append(sample)
        predict = self.SAMPLE_PREDICT.format(counter=len(tales) + 1, text=text)
        output.append(predict)
        return '\n'.join(output)

    def prompt_heroes(self, text: str, as_tale: str = None) -> str:
        """Builds prompt to get heroes description."""
        tales = self.tales
        if as_tale:
            tales = [tale for tale in base_tales.TALES if tale['name'] == as_tale]
        output = []
        for counter, tale in enumerate(tales, 1):
            output.append(self.HEROES.format(
                counter=counter, text=tale['summary'], heroes=tale['heroes']))
        predict = self.HEROES_PREDICT.format(counter=len(tales) + 1, text=text)
        output.append(predict)
        return '\n'.join(output)

    async def get_heroes(self, as_tale: str = None, **kwargs):
        """Generates heroes names and descriptions."""
        prompt = self.prompt_heroes(self.line, as_tale)
        result = await self.generate(prompt, **kwargs)
        output = []
        for idx, gen in enumerate(result['generation'].values):
            heroes = []
            descriptions = re.findall(
                r'\<description\>\s(.*?)\s<stop>', gen, re.DOTALL)
            names = re.findall(
                r'\<character\>\s(.*?)\s<description>', gen, re.DOTALL)
            self.heroes[idx] = {'names': names, 'descriptions': descriptions}
            for hero_id, (name, description) in enumerate(zip(names, descriptions), start=1):
                if description:
                    heroes.append({
                        'id': hero_id,
                        'name': name,
                        'description': description})
            if heroes:
                output.append(heroes)
        return output

    async def get_structure(self, heroes: int = None, **kwargs):
        """Generates tale structure gor given heroes."""
        pattern = re.compile(r"\d\) (.*?)\s\((.*?)\)", re.DOTALL)
        text = [self.line]
        if heroes is not None:
            text.append('\n'.join(self.heroes[heroes]['descriptions']))
        prompt = self.prompt_structure('\n'.join(text))
        output = await self.generate(prompt, **kwargs)
        for idx, gen in enumerate(output['generation'].values):
            matched = re.search(r'(1\).*?)\n\n', gen, re.DOTALL)
            if matched:
                parts = pattern.findall(matched.group())
                parts = [dict(id=part_id, name=name, text=text)
                    for part_id, (name, text) in enumerate(parts, start=1)]
                self.structures[idx] = parts
        return self.structures

    async def get_tale(
            self, as_tale: str, structure: int = None, heroes: int = None,
            **kwargs):
        """Generates final tale text for given heroes and structure."""
        text = [self.line]
        if heroes is not None:
            text.append('\n'.join(self.heroes[heroes]['descriptions']))
        if structure is not None:
            text.append(self.structures[structure])
        prompt = self.prompt_text_as_tale('\n'.join(text), as_tale)
        if not prompt:
            return ''
        result = await self.generate(prompt, **kwargs)
        stories = []
        for idx, story in enumerate(result['generation'].values):
            stories.append(f'{story}')
        return stories
