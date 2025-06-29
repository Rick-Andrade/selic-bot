from abc import ABC, abstractmethod
import json

class AgentBase(ABC):
    """
    Abstract base class for all intelligent agents.
    Provides shared utilities such as prompt and JSON loading.
    """

    def __init__(self, api_key: str, prompt_path: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.system_prompt = self._load_prompt(prompt_path)
        # self.client = self._build_client()

    @abstractmethod
    def generate(self, input_text: str) -> str:
        """
        Generates a response based on the provided input text.

        Args:
            input_text (str): The input text to process.

        Returns:
            str: The generated response as a string.
        """

    def _build_client(self):
        """
        Override in child classes if needed. Defaults to None.
        """
        return None

    def _load_prompt(self, path: str) -> str:
        """
        Loads and returns the contents of a prompt file as a string.

        Args:
            path (str): The file path to the prompt file.

        Returns:
            str: The contents of the prompt file, with leading and trailing whitespace removed.

        Raises:
            RuntimeError: If the prompt file is not found or an error occurs while reading the file.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError as exc:
            raise RuntimeError(f"Prompt file not found at: {path}") from exc
        except Exception as e:
            raise RuntimeError(f"Error reading prompt file: {e}") from e

    def _load_json(self, path: str) -> dict:
        """
        Loads and parses a JSON file from the specified path.

        Args:
            path (str): The file path to the JSON file.

        Returns:
            dict: The parsed JSON data as a dictionary.

        Raises:
            RuntimeError: If the file is not found, cannot be decoded as JSON,
            or another error occurs during reading.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as exc:
            raise RuntimeError(f"File not found at: {path}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Error decoding JSON: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"Error reading JSON file: {exc}") from exc
