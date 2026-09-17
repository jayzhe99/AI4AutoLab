"""从命令行运行离线智能体骨架。"""

import json
import sys
from dataclasses import asdict

from .agent import ReActAgent
from .planner import DemoPlanner
from .safety import ToolGuard
from .tools import CalculatorTool, ToolRegistry


def main() -> int:
    user_input = " ".join(sys.argv[1:]).strip() or "计算: 10 * 0.05"
    agent = ReActAgent(
        planner=DemoPlanner(),
        tools=ToolRegistry([CalculatorTool()]),
        guard=ToolGuard(max_steps=3),
    )
    state = agent.run(user_input)
    print(json.dumps(asdict(state), ensure_ascii=False, indent=2))
    return 0 if state.status.value == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
