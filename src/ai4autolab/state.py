"""智能体循环共享的状态和消息类型。"""

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
    """规划器发出的工具调用请求。"""

    tool_name: str
    arguments: Dict[str, Any]


@dataclass(frozen=True)
class Observation:
    """工具返回的结构化观察结果。"""

    tool_name: str
    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass(frozen=True)
class AgentDecision:
    """规划器每一步只能调用一个工具，或者生成最终回答。"""

    action: Optional[ToolCall] = None
    final_answer: Optional[str] = None

    def __post_init__(self) -> None:
        choices = int(self.action is not None) + int(self.final_answer is not None)
        if choices != 1:
            raise ValueError("一次决策必须且只能包含一个工具动作或一个最终回答。")


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
