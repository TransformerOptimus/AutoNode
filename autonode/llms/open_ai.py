import json
import time
import tiktoken
import openai
from openai import OpenAI
from autonode.logger.logger import logger
from autonode.config.config import get_config
from autonode.llms.base_llm import BaseLlm


class OpenAi(BaseLlm):
    def __init__(self, api_key, model="gpt-4-1106-preview", temperature=1,
                 max_tokens=get_config("MAX_MODEL_TOKEN_LIMIT", 4000), top_p=1, frequency_penalty=0,
                 response_format={"type": "text"}, presence_penalty=0, number_of_results=1):
        """
        Args:
            api_key (str): The OpenAI API key.
            model (str): The model.
            temperature (float): The temperature.
            max_tokens (int): The maximum number of tokens.
            top_p (float): The top p.
            frequency_penalty (float): The frequency penalty.
            presence_penalty (float): The presence penalty.
            number_of_results (int): The number of results.
        """
        super().__init__()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.number_of_results = number_of_results
        self.api_key = api_key
        self.response_format = response_format
        openai.api_key = api_key
        openai.api_base = get_config("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.client = OpenAI(api_key=str(self.api_key))
        self.retry_attempts = 3
        self.backoff_factor = 2
        self.encoding = tiktoken.encoding_for_model(self.model)

    def get_model(self):
        """
        Returns:
            str: The model.
        """
        return self.model

    def chat_completion(self, messages, max_tokens=get_config("MAX_MODEL_TOKEN_LIMIT", 4000),
                        tools=None, tool_choice="auto", response_format={"type": "text"}):
        """
        Call the OpenAI chat completion API.

        Args:
            messages (list): The messages.
            max_tokens (int): The maximum number of tokens.

        Returns:
            dict: The response.
        """

        attempts = 0
        while attempts < self.retry_attempts:
            attempts += 1
            try:
                logger.info(f"OpenAI chat completion retry attempt {attempts}/{self.retry_attempts} ")

                response = self.client.chat.completions.create(
                    n=self.number_of_results,
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=max_tokens,
                    top_p=self.top_p,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty,
                    response_format=response_format,
                    tools=tools,
                )
                content = response.choices[0].message.content
                if response_format["type"] == "json_object":
                    json.loads(content)

                logger.info("LLM RESPONSE : ", content)
                return {
                    "response": response,
                    "content": content
                }

            except Exception as exception:
                logger.info("Exception:", exception)
                if attempts == self.retry_attempts:
                    logger.info("Retries exhausted. Returning the error:", exception)
                    raise exception
                time.sleep(self.backoff_factor ** attempts)