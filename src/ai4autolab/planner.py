"""规划器边界：未来可将DemoPlanner替换为真实大模型规划器。"""

import re
from abc import ABC, abstractmethod
from typing import Dict, List

from .state import AgentDecision, AgentState, ToolCall


class Planner(ABC):
    @abstractmethod
    def decide(
        self, state: AgentState, available_tools: List[Dict[str, str]]
    ) -> AgentDecision:
        """选择一个工具调用，或者直接返回最终回答。"""


class DemoPlanner(Planner):
    """仅用于验证“智能体—工具—观察”闭环的离线规划器。"""

    _calculation_pattern = re.compile(
        r"^(?:calculate|calc|计算)\s*[:：]?\s*(?P<expression>.+)$", re.IGNORECASE
    )

    def decide(
        self, state: AgentState, available_tools: List[Dict[str, str]]
    ) -> AgentDecision:
        if state.observations:
            observation = state.observations[-1]
            if observation.ok:
                return AgentDecision(
                    final_answer="工具 {!r} 返回：{}".format(
                        observation.tool_name, observation.data
                    )
                )
            return AgentDecision(
                final_answer="工具 {!r} 执行失败：{}".format(
                    observation.tool_name, observation.error
                )
            )

        match = self._calculation_pattern.match(state.user_input.strip())
        if match:
            return AgentDecision(
                action=ToolCall(
                    tool_name="calculator",
                    arguments={"expression": match.group("expression")},
                )
            )

        names = [item["name"] for item in available_tools]
        return AgentDecision(
            final_answer=(
                "离线演示规划器无法把该请求映射到工具。"
                "当前可用工具：{}".format(", ".join(names) or "无")
            )
        )
