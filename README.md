# AI4AutoLab

AI4AutoLab 是一个面向自主实验室的“自然语言智能体 + 工具调用”框架，目标是让大模型通过受控工具连接实验软件、机器人运行时和实验硬件。

## 当前阶段

仓库目前包含一个不依赖第三方库的最小骨架，用于在接入真实大模型和实验室硬件之前验证控制闭环：

```text
用户请求
  -> 规划器决策
  -> 已注册工具
  -> 安全检查
  -> 工具执行
  -> 结构化观察结果
  -> 规划器生成最终回答
```

当前的 `DemoPlanner` 是一个确定性的离线演示程序，不是真实大模型，也不具备通用自然语言理解能力。未来接入大模型时，只需要实现相同的 `Planner` 接口。

## 仓库结构

```text
src/ai4autolab/
  agent.py              有最大步数限制的 ReAct 风格循环
  planner.py            规划器接口与离线演示规划器
  state.py              决策、调用、观察结果和智能体状态
  tools/
    base.py             工具统一接口
    registry.py         工具白名单与注册表
    calculator.py       安全的算术演示工具
  safety/
    guard.py            执行前检查和最大步数限制
robot_policies/
  README.md             机器人策略模型的存放与管理说明
tests/
  test_agent.py         离线单元测试
```

## 运行离线演示

无需安装任何第三方Python库。在PowerShell中运行：

```powershell
$env:PYTHONPATH = "src"
python -m ai4autolab "计算: 10 * 0.05"
```

运行测试：

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## 安全边界

所有工具必须显式注册，每次调用都要在执行前验证参数，并且智能体循环有固定的最大步数。当前骨架不会控制真实硬件。未来接入硬件的工具还必须增加仿真、人工授权、超时、工作空间限制和急停检查。

## 工具与机器人策略的区别

工具（Tool）是提供给大模型调用的受控操作，例如计算器、数据库查询或未来的 `LeRobotExecutionTool`。机器人策略（Robot Policy）是训练得到的模型，负责把相机图像、关节状态等观察转换成机器人动作。

智能体调用工具，工具启动机器人运行时，机器人运行时再加载并执行指定的机器人策略：

```text
大模型智能体 -> 工具 -> LeRobot运行时 -> 机器人策略 -> 机器人硬件
```

## 下一阶段

用一次真实的HTTP模型请求替换 `DemoPlanner`，让模型输出结构化工具调用或最终回答。计算和设备行为继续放在可测试的确定性工具中，不让大模型直接执行任意代码或硬件命令。
