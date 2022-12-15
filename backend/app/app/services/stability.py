import io
import os
import logging
import requests

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from app.core.config import settings

logger = logging.getLogger('uvicorn')
API_KEY = settings.STABILITY_KEY

NON_URL_SAFE = [
    '"', '#', '$', '%', '&', '+',
    ',', '/', ':', ';', '=', '?',
    '@', '[', '\\', ']', '^', '`',
    '{', '|', '}', '~', "'"]


def _clean_prompt(prompt: str) -> str:
    return prompt.replace('\n', ' ').replace(',', '').replace('.', '')


class StabilityPrompt:
    """Implements client to stability service for image generation."""
    STYLES = {
        'MODERN': (
            '{}, d & d, fantasy, intricate, elegant, '
            'highly detailed, digital painting, artstation, concept art, '
            'matte, sharp focus, illustration, hearthstone, art by artgerm '
            'and greg rutkowski and alphonse mucha '),
        'STEAMPUNK': (
            '{}, beautifully lit, steampunk, by rebecca guay, '
            'by francois schuiten '),
        'ELF': (
            '{}, hand drawn cute gnomes in autumn disguise holding pumpkin '
            'and maple leaf, detailed, concept art, low angle, high detail, '
            'warm lighting, volumetric, godrays, vivid, beautiful, trending '
            'on artstation, by jordan grimmer, huge scene, grass, art greg '
            'rutkowski '),
        'BW': (
            '{}, in the style of h. r. giger, horror, dark, grain, realistic '
            'lighting, monochromatic '),
        'XMAS': (
            '{}, an extremely detailed concept art of a spiritual fantasy jingle '
            'bell infused with magic, trending on artstation, digital art, '
            '4 k, intricate, octane render, sharp focus '),
        'PIXAR': (
            '{}, a wholesome animation key shot of hogsmeade, colorful, pixar and '
            'disney animation, sharp, very detailed, high resolution, key '
            'art by greg rutkowski, bloom, dramatic lighting ')
    }

    def __init__(self):
        logger.info('Init stability with server HOST: %s', settings.SERVER_HOST)
        self._translate_table = {ord(char): '' for char in NON_URL_SAFE}
        self.client = client.StabilityInference(key=API_KEY, verbose=True)

    def _get_style(self, style: str) -> str:
        if style in self.STYLES.keys():
            return self.STYLES[style]
        return self.STYLES['MODERN']

    def _slugify(self, text) -> str:
        text = text.translate(self._translate_table)
        text = '-'.join(text.split())
        return text[:255]

    def _save_image(self, prompt: str, image_data) -> tuple[str, str]:
        url = os.path.join(settings.SERVER_HOST, 'upload')
        files = {'file': (self._slugify(prompt), image_data, 'image/png')}
        response = requests.post(url, files=files)
        data = response.json()
        return data.get('file_uid'), data.get('path')

    def generate_character(self, hero_id: int, prompt: str, **kwargs):
        """Returns list of generated images."""
        prompt = _clean_prompt(prompt)
        style = kwargs.get('style', 'classic')
        style = self._get_style(style)
        params = {
            'steps': 20,
            'guidance_strength': 0.5
        }
        logger.info('generating portrait:%s\n params:%s', prompt, params)
        answers = self.client.generate(
            prompt=style.format(prompt), **params)

        images = []
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    logger.warning(
                        'Your request activated the API\'s safety filters '
                        'and could not be processed.'
                        'Please modify the prompt and try again.')
                if artifact.type == generation.ARTIFACT_IMAGE:
                    uid, path = self._save_image(
                        prompt, io.BytesIO(artifact.binary))
                    images.append({
                        'uid': uid,
                        'path': path,
                        'style': style,
                        'prompt': prompt,
                        'hero_id': hero_id})
        return images

    def generate_scene(self, scene_id: int, prompt: str, **kwargs):
        """Returns list of generated images."""
        prompt = _clean_prompt(prompt)
        style = kwargs.get('style', 'classic')
        style = self._get_style(style)
        params = {
            'samples': 1,
            'steps': 20,
            'guidance_strength': 0.25,
        }
        logger.info('generating scene:%s\n params:%s', prompt, params)
        answers = self.client.generate(
            prompt=style.format(prompt), **params)

        images = []
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    logger.warning(
                        'Your request activated the API\'s safety filters '
                        'and could not be processed.'
                        'Please modify the prompt and try again.')
                if artifact.type == generation.ARTIFACT_IMAGE:
                    uid, path = self._save_image(
                        prompt, io.BytesIO(artifact.binary))
                    images.append({
                        'uid': uid,
                        'path': path,
                        'style': style,
                        'prompt': prompt,
                        'scene_id': scene_id})
        return images
