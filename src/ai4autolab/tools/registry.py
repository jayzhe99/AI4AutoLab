"""智能体允许调用的工具白名单。"""

from typing import Dict, Iterable, List

from .base import Tool, ToolError


class ToolRegistry:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._tools: Dict[str, Tool] = {}
        for tool in tools:
            self.register(tool)

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ToolError("工具 {!r} 已经注册。".format(tool.name))
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolError("工具 {!r} 尚未注册。".format(name)) from exc

    def specifications(self) -> List[Dict[str, str]]:
        return [tool.specification() for tool in self._tools.values()]
