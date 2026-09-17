"""Planner boundary: replace DemoPlanner with an LLM-backed planner later."""

import re
from abc import ABC, abstractmethod
from typing import Dict, List

from .state import AgentDecision, AgentState, ToolCall


class Planner(ABC):
    @abstractmethod
    def decide(
        self, state: AgentState, available_tools: List[Dict[str, str]]
    ) -> AgentDecision:
        """Choose one tool call or return a final answer."""


class DemoPlanner(Planner):
    """Offline planner used only to verify the agent-tool-observation loop."""

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
                    final_answer="Tool {!r} returned: {}".format(
                        observation.tool_name, observation.data
                    )
                )
            return AgentDecision(
                final_answer="Tool {!r} failed: {}".format(
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
                "The offline demo planner could not map this request to a tool. "
                "Available tools: {}".format(", ".join(names) or "none")
            )
        )
