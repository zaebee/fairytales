"""Implements tales generator on Cohere service."""

import re
import os
import cohere
import pandas as pd

from app.services import tales as base_tales

COHERE_KEY = 'onk1aMdIZZ4P86E99JlD095UEVH7LfIUwwmEF7KQ'
STABILITY_KEY = 'sk-kKDdwGtHoPO4kiOSWQck3D1TEaBRRAVMUPhdKyHUN9A0DVH3'

# Paste your API key here. Remember to not share it publicly
os.environ['COHERE_KEY'] = COHERE_KEY

CohereError = cohere.CohereError


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
        self.client = None
        self.heroes = {}
        self.structures = {}
        self.line = line
        self.as_tale = as_tale
        self.tales = kwargs.get('tales', base_tales.TALES)

    async def close(self):
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
        params = {
            'return_likelihoods': 'GENERATION',
            'stop_sequences': stop_sequences or ['<end>'],
            'max_tokens': kwargs.get('max_tokens', 50),
            'num_generations': kwargs.get('', 5),
            'temperature': kwargs.get('temperature', 0.7),
        }
        prediction = await self.client.generate(
            model=model, prompt=prompt, **params)
        gens = []
        likelihoods = []
        for gen in prediction.generations:
            gens.append(gen.text)

            sum_likelihood = 0
            for token in gen.token_likelihoods:
                sum_likelihood += token.likelihood
            likelihoods.append(sum_likelihood)

        data = pd.DataFrame({'generation':gens, 'likelihood': likelihoods})
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
            tales = [tale for tale in self.tales if tale['name'] == as_tale]
        output = []
        for counter, tale in enumerate(tales, 1):
            output.append(self.HEROES.format(
                counter=counter, text=tale['summary'], heroes=tale['heroes']))
        predict = self.HEROES_PREDICT.format(counter=len(tales) + 1, text=text)
        output.append(predict)
        return '\n'.join(output)

    async def get_heroes(self, as_tale: str = None, max_tokens: int = 500):
        """Generates heroes names and descriptions."""
        prompt = self.prompt_heroes(self.line, as_tale)
        result = await self.generate(
            prompt, num_generations=3, temperature=0.618,
            max_tokens=max_tokens)
        for idx, gen in enumerate(result['generation'].values):
            descriptions = re.findall(
                r'\<description\>\s(.*?)\s<stop>', gen, re.DOTALL)
            names = re.findall(
                r'\<character\>\s(.*?)\s<description>', gen, re.DOTALL)
            self.heroes[idx] = {'names': names, 'descriptions': descriptions}
        return self.heroes

    async def get_structure(self, heroes: int = None, max_tokens: int = 500):
        """Generates tale structure gor given heroes."""
        text = [self.line]
        if heroes is not None:
            text.append('\n'.join(self.heroes[heroes]['descriptions']))
        prompt = self.prompt_structure('\n'.join(text))
        output = await self.generate(
            prompt, num_generations=3, temperature=0.88, max_tokens=max_tokens)
        for idx, gen in enumerate(output['generation'].values):
            matched = re.search(r'(1\).*?)\n\n', gen, re.DOTALL)
            if matched:
                self.structures[idx] = matched.group()
        return self.structures

    async def get_tale(
        self, as_tale: str, structure: int = None, heroes: int = None,
        max_tokens: int = 500):
        """Generates final tale text for given heroes and structure."""
        text = [self.line]
        if heroes is not None:
            text.append('\n'.join(self.heroes[heroes]['descriptions']))
        if structure is not None:
            text.append(self.structures[structure])
        prompt = self.prompt_text_as_tale('\n'.join(text), as_tale)
        if not prompt:
            return ''
        result = await self.generate(
            prompt, num_generations=3, temperature=0.88, max_tokens=max_tokens)
        stories = []
        for idx, story in enumerate(result['generation'].values):
            stories.append(f'Story: {idx}\n{story}\n==========\n')
        return '\n'.join(stories)
