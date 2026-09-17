"""Central pre-execution guard for agent tool calls."""

from ai4autolab.state import AgentState, ToolCall
from ai4autolab.tools.base import Tool, ToolError


class ToolGuard:
    def __init__(self, max_steps: int = 5) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1.")
        self.max_steps = max_steps

    def check_step_budget(self, state: AgentState) -> None:
        if len(state.steps) >= self.max_steps:
            raise ToolError("Agent reached the maximum tool-call budget.")

    def validate_call(self, call: ToolCall, tool: Tool) -> None:
        if call.tool_name != tool.name:
            raise ToolError("Resolved tool does not match the requested tool.")
        tool.validate(call.arguments)
