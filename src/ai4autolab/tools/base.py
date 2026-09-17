"""Common interface implemented by every agent-callable tool."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class ToolError(ValueError):
    """Raised when a tool call is invalid or cannot be executed safely."""


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def validate(self, arguments: Dict[str, Any]) -> None:
        """Reject malformed or unsafe arguments before execution."""

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool and return a JSON-compatible observation."""

    def specification(self) -> Dict[str, str]:
        return {"name": self.name, "description": self.description}

