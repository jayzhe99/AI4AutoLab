"""Minimal bounded ReAct-style agent loop."""

from .planner import Planner
from .safety.guard import ToolGuard
from .state import AgentState, AgentStatus, AgentStep, Observation
from .tools.base import ToolError
from .tools.registry import ToolRegistry


class ReActAgent:
    def __init__(
        self,
        planner: Planner,
        tools: ToolRegistry,
        guard: ToolGuard,
    ) -> None:
        self.planner = planner
        self.tools = tools
        self.guard = guard

    def run(self, user_input: str) -> AgentState:
        state = AgentState(user_input=user_input, status=AgentStatus.RUNNING)

        while state.status == AgentStatus.RUNNING:
            try:
                self.guard.check_step_budget(state)
                decision = self.planner.decide(
                    state, self.tools.specifications()
                )

                if decision.final_answer is not None:
                    state.steps.append(
                        AgentStep(index=len(state.steps) + 1, decision=decision)
                    )
                    state.final_answer = decision.final_answer
                    state.status = AgentStatus.COMPLETED
                    continue

                call = decision.action
                if call is None:
                    raise ToolError("Planner returned neither action nor final answer.")

                tool = self.tools.get(call.tool_name)
                self.guard.validate_call(call, tool)
                result = tool.execute(call.arguments)
                observation = Observation(
                    tool_name=tool.name,
                    ok=True,
                    data=result,
                )
                state.steps.append(
                    AgentStep(
                        index=len(state.steps) + 1,
                        decision=decision,
                        observation=observation,
                    )
                )
            except ToolError as exc:
                state.status = AgentStatus.BLOCKED
                state.final_answer = str(exc)

        return state
