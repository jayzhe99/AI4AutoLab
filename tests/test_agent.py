import unittest

from ai4autolab.agent import ReActAgent
from ai4autolab.planner import DemoPlanner
from ai4autolab.safety import ToolGuard
from ai4autolab.state import AgentStatus
from ai4autolab.tools import CalculatorTool, ToolError, ToolRegistry


class CalculatorToolTests(unittest.TestCase):
    def test_basic_arithmetic(self) -> None:
        tool = CalculatorTool()
        arguments = {"expression": "10 * 0.05"}
        tool.validate(arguments)
        self.assertEqual(tool.execute(arguments)["result"], 0.5)

    def test_rejects_function_calls(self) -> None:
        tool = CalculatorTool()
        with self.assertRaises(ToolError):
            tool.validate({"expression": "__import__('os').system('echo unsafe')"})


class AgentLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = ReActAgent(
            planner=DemoPlanner(),
            tools=ToolRegistry([CalculatorTool()]),
            guard=ToolGuard(max_steps=3),
        )

    def test_tool_call_and_observation(self) -> None:
        state = self.agent.run("计算: 10 * 0.05")
        self.assertEqual(state.status, AgentStatus.COMPLETED)
        self.assertEqual(state.observations[0].data["result"], 0.5)
        self.assertEqual(len(state.steps), 2)

    def test_unknown_request_finishes_without_action(self) -> None:
        state = self.agent.run("请帮我设计一个实验")
        self.assertEqual(state.status, AgentStatus.COMPLETED)
        self.assertEqual(state.observations, [])


if __name__ == "__main__":
    unittest.main()
