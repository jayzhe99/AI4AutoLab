"""智能体工具调用的统一执行前检查。"""

from ai4autolab.state import AgentState, ToolCall
from ai4autolab.tools.base import Tool, ToolError


class ToolGuard:
    def __init__(self, max_steps: int = 5) -> None:
        if max_steps < 1:
            raise ValueError("max_steps必须大于或等于1。")
        self.max_steps = max_steps

    def check_step_budget(self, state: AgentState) -> None:
        if len(state.steps) >= self.max_steps:
            raise ToolError("智能体已达到最大工具调用次数。")

    def validate_call(self, call: ToolCall, tool: Tool) -> None:
        if call.tool_name != tool.name:
            raise ToolError("解析出的工具与请求调用的工具不一致。")
        tool.validate(call.arguments)
