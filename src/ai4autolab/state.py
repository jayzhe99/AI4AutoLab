"""State and message types shared by the agent loop."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentStatus(str, Enum):
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True)
class ToolCall:
    """A planner request to execute one registered tool."""

    tool_name: str
    arguments: Dict[str, Any]


@dataclass(frozen=True)
class Observation:
    """The structured result returned by a tool."""

    tool_name: str
    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass(frozen=True)
class AgentDecision:
    """A planner may request an action or finish with a user-facing answer."""

    action: Optional[ToolCall] = None
    final_answer: Optional[str] = None

    def __post_init__(self) -> None:
        choices = int(self.action is not None) + int(self.final_answer is not None)
        if choices != 1:
            raise ValueError("A decision must contain exactly one action or final answer.")


@dataclass
class AgentStep:
    index: int
    decision: AgentDecision
    observation: Optional[Observation] = None


@dataclass
class AgentState:
    user_input: str
    status: AgentStatus = AgentStatus.READY
    steps: List[AgentStep] = field(default_factory=list)
    final_answer: Optional[str] = None

    @property
    def observations(self) -> List[Observation]:
        return [step.observation for step in self.steps if step.observation is not None]
