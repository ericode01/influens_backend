import time
import openai
from openai.error import APIError, RateLimitError, Timeout
from colorama import Fore
from llm.base import Message


class OpenAIWrapper:

    def __init__(self):
        self.use_azure = False
        self.openai_api_key = "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"

    # Overly simple abstraction until we create something better
    # simple retry mechanism when getting a rate error or a bad gateway
    def create_chat_completion(
            self,
            messages: list[Message],  # type: ignore
            model: str | None = None,
            temperature: float = None,
            max_tokens: int | None = None,
    ) -> str:
        """Create a chat completion using the OpenAI API

        Args:
            messages (List[Message]): The messages to send to the chat completion
            model (str, optional): The model to use. Defaults to None.
            temperature (float, optional): The temperature to use. Defaults to 0.9.
            max_tokens (int, optional): The max tokens to use. Defaults to None.

        Returns:
            str: The response from the chat completion
        """
        num_retries = 10

        response = None
        for attempt in range(num_retries):
            backoff = 2 ** (attempt + 2)
            try:
                if self.use_azure:
                    response = self.get_response_from_openai(
                        deployment_id="",
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                else:
                    print(
                        f"create_chat_completion() Attempt {attempt}. Model: {model}. temperature: {temperature}. max_tokens: {max_tokens}. Messages: {messages}")
                    response = self.get_response_from_openai(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                break
            except RateLimitError:
                print(
                    f"{Fore.RED}Error: ", f"Reached rate limit, passing...{Fore.RESET}"
                )
            except (APIError, Timeout) as e:
                if e.http_status != 502:
                    raise
                if attempt == num_retries - 1:
                    raise
            print(
                f"{Fore.RED}Error: ",
                f"API Bad gateway. Waiting {backoff} seconds...{Fore.RESET}",
            )
            time.sleep(backoff)

        if response is None:
            print(
                "FAILED TO GET RESPONSE FROM OPENAI",
                Fore.RED,
                "Auto-GPT has failed to get a response from OpenAI's services. "
                + f"Try running Auto-GPT again, and if the problem the persists try running it with `{Fore.CYAN}--debug{Fore.RESET}`.",
            )
            resp = "Failed to get response from OpenAI. Please retry."
        else:
            resp = response.choices[0].message["content"]

        return resp

    def get_response_from_openai(
            self,
            messages: list,  # type: ignore
            model: str | None = None,
            temperature: float = None,
            max_tokens: int | None = None,
            deployment_id=None,
    ) -> str:
        """
        Create a chat completion and update the cost.
        Args:
        messages (list): The list of messages to send to the API.
        model (str): The model to use for the API call.
        temperature (float): The temperature to use for the API call.
        max_tokens (int): The maximum number of tokens for the API call.
        Returns:
        str: The AI's response.
        """
        if temperature is None:
            temperature = 0.0

        if deployment_id is not None:
            response = openai.ChatCompletion.create(
                deployment_id=deployment_id,
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=self.openai_api_key,
            )
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=self.openai_api_key,
            )
        print(f"[OpenAIWrapper.get_response_from_openai] Response: {response}")
        # prompt_tokens = response.usage.prompt_tokens
        # completion_tokens = response.usage.completion_tokens
        # self.update_cost(prompt_tokens, completion_tokens, model)
        return response
