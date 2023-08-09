from typing import List
from typing import Optional

from pydantic import Field

from processors.providers.api_processor_interface import ApiProcessorInterface
from processors.providers.api_processor_interface import BaseSchema
from processors.providers.replicate.utils import fetch_data_from_api
from common.utils.utils import get_key_or_raise


class GenericInput(BaseSchema):
    model: str = Field(..., description='Model name')
    version: str = Field(..., description='Model version')


class GenericConfiguration(BaseSchema):
    sync_mode: Optional[bool] = Field(
        False, description='Run in synchronous mode',
    )


class GenericOutput(BaseSchema):
    generations: List[dict] = Field(
        default=[], description='The completions generated by the model.',
    )
    _api_response: dict = Field(
        default={}, description='The raw response from the API.',
    )


class Generic(ApiProcessorInterface[GenericInput, GenericOutput, GenericConfiguration]):
    def name() -> str:
        return 'replicate/generic'

    def process(self) -> dict:
        _env = self._env
        replicate_api_key = get_key_or_raise(
            _env, 'replicate_api_key', 'No replicate_api_key found in _env',
        )

        url = 'https://api.replicate.com/v1/predictions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {replicate_api_key}',
        }
        configuration = self._config.dict().pop('sync_mode')
        api_params = {
            'version': self._input.version,
            'input': {**self._input.dict()},
        }
        api_params.pop('_env', None)

        api_response = fetch_data_from_api(url, api_params, headers)

        if api_response.ok:
            json_api_response = api_response.json()
            result = {
                'async': json_api_response['urls'], '_response': {
                    '_api_response': json_api_response,
                },
            }
            return result
        else:
            raise Exception(f'Error calling OpenAI API: {api_response.text}')
