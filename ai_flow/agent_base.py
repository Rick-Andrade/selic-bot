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
        self.client = self._build_client()

    @abstractmethod
    def generate(self, input_text: str) -> str:
        pass

    def _build_client(self):
        """
        Override in child classes if needed. Defaults to None.
        """
        return None

    def _load_prompt(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise RuntimeError(f"Prompt file not found at: {path}")
        except Exception as e:
            raise RuntimeError(f"Error reading prompt file: {e}")

    def _load_json(self, path: str) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise RuntimeError(f"File not found at: {path}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error decoding JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Error reading JSON file: {e}")
