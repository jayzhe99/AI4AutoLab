# AI4AutoLab

AI4AutoLab is an LLM-tool framework for building flexible, skill-driven
autonomous laboratories.

## Current milestone

The repository currently contains a small, dependency-free skeleton that proves
the control loop before a real LLM or laboratory hardware is connected:

```text
user request
  -> planner decision
  -> registered tool
  -> safety guard
  -> tool execution
  -> structured observation
  -> planner final answer
```

The included `DemoPlanner` is deliberately deterministic. It is not an LLM and
does not claim to understand general natural language. A future LLM-backed
planner will implement the same `Planner` interface.

## Repository layout

```text
src/ai4autolab/
  agent.py              bounded ReAct-style control loop
  planner.py            planner interface and offline demo planner
  state.py              decisions, calls, observations and agent state
  tools/
    base.py             common tool contract
    registry.py         explicit tool allowlist
    calculator.py       safe arithmetic example tool
  safety/
    guard.py            pre-execution checks and step budget
tests/
  test_agent.py         offline unit tests
```

## Run the offline demo

No third-party package is required. In PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m ai4autolab "计算: 10 * 0.05"
```

Run tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Safety boundary

Tools are registered explicitly. Every call is validated before execution,
and the loop has a fixed step budget. The skeleton does not control real
hardware. Hardware tools must later add simulation, authorization, timeout,
workspace and emergency-stop checks.

## Tools and robot policies

An agent tool is a callable operation exposed to the LLM, such as a calculator,
database query or `LeRobotExecutionTool`. A robot policy is a trained model that
maps robot observations to actions. The agent calls a tool; the tool starts the
robotics runtime; the runtime executes the selected robot policy.

```text
LLM Agent -> Tool -> LeRobot runtime -> Robot Policy -> Robot hardware
```

## Next milestone

Replace `DemoPlanner` with one real HTTP model call that returns either a
structured tool call or a final answer. Keep calculation and device behavior
inside deterministic tools rather than asking the model to execute them.
