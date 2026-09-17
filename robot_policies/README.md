# Robot Policies

This directory documents trained robot policies. A robot policy maps robot
observations to actions and is executed by a robotics runtime such as LeRobot.
It is not an LLM tool.

Large datasets and model checkpoints should not be committed to normal Git
history. Keep only small manifests and evaluation summaries here. Store model
artifacts locally, with Git LFS, DVC, a model registry, or an object store.

An agent-facing tool such as `LeRobotExecutionTool` may select an approved robot
policy and start the robotics runtime. The tool and policy remain separate:

```text
LLM Agent -> Tool -> LeRobot runtime -> Robot Policy -> Robot hardware
```

