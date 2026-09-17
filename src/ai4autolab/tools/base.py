"""所有智能体工具都要实现的统一接口。"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class ToolError(ValueError):
    """工具调用参数无效或无法安全执行时抛出的异常。"""


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def validate(self, arguments: Dict[str, Any]) -> None:
        """在执行前拒绝格式错误或不安全的参数。"""

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具并返回可序列化为JSON的观察结果。"""

    def specification(self) -> Dict[str, str]:
        return {"name": self.name, "description": self.description}
