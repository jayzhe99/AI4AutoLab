"""Explicit allowlist of tools available to an agent."""

from typing import Dict, Iterable, List

from .base import Tool, ToolError


class ToolRegistry:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._tools: Dict[str, Tool] = {}
        for tool in tools:
            self.register(tool)

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ToolError("Tool {!r} is already registered.".format(tool.name))
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolError("Tool {!r} is not registered.".format(name)) from exc

    def specifications(self) -> List[Dict[str, str]]:
        return [tool.specification() for tool in self._tools.values()]

