import logging
from typing import Optional

from asgiref.sync import async_to_sync
from pydantic import Field

from common.promptly.blocks.http import HttpAPIProcessor as CoreHttpAPIProcessor
from common.promptly.blocks.http import HttpAPIProcessorConfiguration
from common.promptly.blocks.http import HttpAPIProcessorInput
from common.promptly.blocks.http import HttpAPIProcessorOutput
from processors.providers.api_processor_interface import ApiProcessorInterface
from processors.providers.api_processor_interface import BaseSchema

logger = logging.getLogger(__name__)


class PromptlyHttpAPIProcessorInput(HttpAPIProcessorInput, BaseSchema):
    pass


class PromptlyHttpAPIProcessorOutput(HttpAPIProcessorOutput, BaseSchema):
    content: Optional[bytes] = Field(widget='hidden')


class PromptlyHttpAPIProcessorConfiguration(HttpAPIProcessorConfiguration, BaseSchema):
    timeout: Optional[int] = Field(
        description='Timeout in seconds', default=5, example=10, advanced_parameter=False, ge=0, le=60,
    )


class PromptlyHttpAPIProcessor(ApiProcessorInterface[PromptlyHttpAPIProcessorInput, PromptlyHttpAPIProcessorOutput, PromptlyHttpAPIProcessorConfiguration]):
    def slug() -> str:
        return 'promptly_http_api_processor'

    def session_data_to_persist(self) -> dict:
        return {}

    def process(self) -> PromptlyHttpAPIProcessorOutput:
        request = HttpAPIProcessorInput(
            url=self._input.url, method=self._input.method, headers=self._input.headers or {}, body=self._input.body, authorization=self._input.authorization,
        )
        response = CoreHttpAPIProcessor(
            PromptlyHttpAPIProcessorConfiguration(allow_redirects=self._config.allow_redirects, timeout=self._config.timeout).dict(),
        ).process(request.dict())

        async_to_sync(self._output_stream.write)(
            PromptlyHttpAPIProcessorOutput(
                code=200, text=response.text, content_json=response.content_json, is_ok=response.is_ok, headers=response.headers,
            ),
        )
        output = self._output_stream.finalize()
        return output
