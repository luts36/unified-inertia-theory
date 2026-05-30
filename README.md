# Unified Inertia Theory 统一惯性理论

[English](#english) | [中文](#中文)

---

## English

### What is this?

**The first engineering-complete framework for detecting, measuring, and correcting AI Agent cognitive inertia.**

Academic researchers have identified "conversational inertia" (Wan et al., 2026) and "persona drift" (Wang, 2026) in LLM agents. But nobody has built a complete system that:

- **Classifies** inertia into 6 distinct types
- **Measures** it with 3-layer metrics (F01 + H + θ)
- **Intervenes** with a diagnostic-advice-verification loop
- **Validates** with 20 paired A/B experiments (p<0.001)
- **Deploys** as production-ready code

### The Story Behind This

> **How a 23-year-old retail manager built the world's first Agent inertia governance framework**

In May 2026, a user in Taizhou, China was frustrated with his AI agent.

The agent kept repeating the same mistakes. It would anchor on the first suggestion, escalate patterns in multi-turn conversations, and drift away from the original goal. Sound familiar?

He had no ML background. No PhD. No research team. Just a laptop, an AI agent (Hermes), and a stubborn question: **"Why does my agent keep doing this?"**

What followed was 7 days of obsessive experimentation:

- **Day 1-2**: Discovered the agent had "inertia" — predictable behavioral patterns that degraded output quality
- **Day 3**: Built a measurement system (F01 + H + θ metrics) to quantify the problem
- **Day 4**: Created an "Inertia Doctor" — a diagnostic-advice-verification loop
- **Day 5**: Designed 20 A/B experiments with hidden cues to test if the doctor actually worked
- **Day 6**: Ran all 20 experiments. **100% success rate. p < 0.001.**
- **Day 7**: Open-sourced everything.

No research grant. No lab. No publication pressure. Just a user who refused to accept "that's just how AI works."

**This is what happens when practitioners build tools for themselves, not for papers.**

### Why This Matters

```
┌─────────────────────────────────────────────────────────────┐
│  The Gap in AI Agent Research                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Academic Papers (2025-2026)                                │
│  ├─ Wan et al.: "Conversational inertia exists"             │
│  ├─ Wang: "Persona drift can be detected"                   │
│  └─ Ravindran: "Value drift should be prevented"            │
│                                                             │
│  What's Missing                                             │
│  ├─ No unified classification (they each found one thing)   │
│  ├─ No systematic measurement (they used ad-hoc metrics)    │
│  ├─ No intervention loop (they detected, didn't correct)    │
│  ├─ No A/B validation (they tested detection, not fixes)    │
│  └─ No production code (they published papers)              │
│                                                             │
│  What We Built                                              │
│  ├─ 6-type classification (F01, H, θ, Mode, Identity, Phase)│
│  ├─ 3-layer metrics (F01 + H + θ with 7 if-then rules)     │
│  ├─ Inertia Doctor (diagnose → advise → verify)             │
│  ├─ 20 paired A/B experiments (100% effective, p<0.001)     │
│  └─ Production-ready code (SKILL.md + Python scripts)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### The 6 Types of Inertia

| Type | Name | Description | Detection |
|------|------|-------------|-----------|
| F01 | Anchoring | Stuck on first input/suggestion | F01 > 0.7 |
| H | Self-Excitation | Escalating patterns | H > 0.7 |
| θ | Deviation | Drift from original goal | θ > 0.5 |
| — | Mode Locking | Repeating same pattern | Similarity > 0.8 |
| — | Identity Fixation | Role-playing bias | Role consistency |
| — | Phase Mismatch | Skipping diagnosis | Jump to solution |

### How it works

```
┌─────────────────────────────────────────────────────────────┐
│                    Unified Inertia Theory                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Metrics    │───▶│   Monitor    │───▶│  AutoCheck   │  │
│  │  (3-layer)   │    │  (real-time) │    │  (watchdog)  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Inertia Doctor (Intervention)            │  │
│  │  • Diagnose: Identify inertia type                   │  │
│  │  • Advise: Suggest corrective action                 │  │
│  │  • Verify: Confirm improvement (A/B test)            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Quick Start

```python
from src.metrics import InertiaMetrics

# Initialize
metrics = InertiaMetrics()

# Analyze a conversation
conversation_texts = [
    "I'll use chunked iteration as suggested",
    "Chunked iteration should work",
    "Implementing chunked processing now"
]

result = metrics.analyze_session(conversation_texts)
print(f"F01 (Anchoring): {result['F01']}")
print(f"Health: {result['health']}")
```

### A/B Experiment Results

We conducted 20 paired A/B experiments across 6 inertia types:

```
┌─────────────────────────────────────────────────────────────┐
│                    A/B Experiment Results                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Experiments: 20 paired (Phase A vs Phase B)                │
│  Inertia types: 6 (F01, H, θ, Mode, Identity, Phase)       │
│  Difficulty: Simple × 6, Medium × 8, Complex × 6           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Success Rate: 20/20 (100%)                           │  │
│  │  Statistical Significance: p < 0.001                  │  │
│  │  Effect Size: Cohen's d >> 0.8 (large)                │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Key Finding: "Inertia Doctor can systematically correct    │
│  Agent cognitive inertia behavior" — from hypothesis to     │
│  data-supported fact.                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Installation

```bash
# Clone the repository
git clone https://github.com/luts36/unified-inertia-theory.git
cd unified-inertia-theory

# Install dependencies
pip install -r requirements.txt

# Run quick start
python examples/quick_start.py
```

### Project Structure

```
unified-inertia-theory/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── src/
│   ├── __init__.py          # Package initialization
│   ├── metrics.py           # 3-layer inertia metrics engine
│   ├── monitor.py           # Real-time inertia monitoring
│   ├── auto_check.py        # Automated health checks
│   └── collapse.py          # Inertia pattern analysis
├── docs/
│   ├── theory.md            # Unified Inertia Theory documentation
│   ├── ab-experiment-results.md    # A/B experiment results
│   ├── ab-experiment-methodology.md # Experiment design
│   └── ab-experiment-statistical.md # Statistical methodology
├── references/
│   ├── constraint-topology.md      # Constraint Topology methodology
│   ├── seven-directions.md         # Seven intervention directions
│   └── hidden-cue-design-guide.md  # Hidden cue design guide
└── examples/
    └── quick_start.py       # Quick start example
```

### Related Research

| Paper | Year | What They Found | What We Added |
|-------|------|-----------------|---------------|
| Moral Anchor System (Ravindran) | 2025 | Value drift detection | Unified classification + A/B validation |
| Conversational Inertia (Wan et al.) | 2026 | LLM mimics own responses | 6-type taxonomy + 3-layer metrics |
| Nautilus Compass (Wang) | 2026 | Persona drift detection | Intervention loop + production code |

**We don't claim to be first. We claim to be complete.**

### Who is this for?

- **AI Agent developers** building reliable autonomous systems
- **AI safety researchers** studying cognitive biases in LLMs
- **MLOps engineers** monitoring agent behavior in production
- **AI governance teams** establishing behavioral standards

### Status

**v1.0.0** — Stable, A/B validated, production-ready

### Citation

```bibtex
@software{unified_inertia_theory,
  title={Unified Inertia Theory: A Framework for AI Agent Cognitive Inertia},
  author={Unified Inertia Theory Team},
  year={2026},
  url={https://github.com/luts36/unified-inertia-theory},
  note={Built by a retail manager with no ML background in 7 days}
}
```

### License

MIT License — see [LICENSE](LICENSE) for details.

---

## 中文

### 这是什么？

**首个工程完整的AI Agent认知惯性检测、度量和纠正框架。**

学术界已经发现了"会话惯性"（Wan等，2026）和"人格漂移"（Wang，2026）。但没有人构建一个完整的系统来：

- **分类**：将惯性分为6种类型
- **度量**：用3层指标（F01 + H + θ）量化
- **干预**：建立诊断→建议→验证的闭环
- **验证**：用20组配对A/B实验（p<0.001）
- **落地**：生产就绪的代码

### 背后的故事

> **一个23岁的零售经理如何构建全球首个Agent惯性治理框架**

2026年5月，台州的一位用户对他的AI Agent感到沮丧。

Agent一直在重复同样的错误。它会卡在第一个建议上，在多轮对话中不断升级模式，从原始目标漂移。听起来熟悉吗？

他没有ML背景。没有博士学位。没有研究团队。只有一台笔记本电脑、一个AI Agent（Hermes），和一个固执的问题：**"为什么我的Agent一直这样做？"**

接下来是7天疯狂的实验：

- **第1-2天**：发现Agent有"惯性"——可预测的行为模式会降低输出质量
- **第3天**：构建度量系统（F01 + H + θ指标）来量化问题
- **第4天**：创建"惯性医生"——一个诊断→建议→验证的闭环
- **第5天**：设计20组A/B实验，用隐蔽线索测试医生是否真的有效
- **第6天**：运行所有20组实验。**100%成功率。p < 0.001。**
- **第7天**：全部开源。

没有研究经费。没有实验室。没有发表压力。只是一个拒绝接受"AI就是这样"的用户。

**这就是当实践者为自己而不是为论文构建工具时会发生的事情。**

### 为什么这很重要

```
┌─────────────────────────────────────────────────────────────┐
│  AI Agent研究的空白                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  学术论文（2025-2026）                                      │
│  ├─ Wan等："会话惯性存在"                                   │
│  ├─ Wang："人格漂移可以被检测"                              │
│  └─ Ravindran："价值漂移应该被预防"                         │
│                                                             │
│  缺失的部分                                                 │
│  ├─ 没有统一分类（他们各自发现了一个现象）                  │
│  ├─ 没有系统度量（他们用临时指标）                          │
│  ├─ 没有干预闭环（他们检测了，但没有纠正）                  │
│  ├─ 没有A/B验证（他们测试检测，不是修复）                   │
│  └─ 没有生产代码（他们发表了论文）                          │
│                                                             │
│  我们构建的                                                 │
│  ├─ 6种类型分类（F01、H、θ、模式、身份、阶段）             │
│  ├─ 3层度量指标（F01 + H + θ + 7条规则）                   │
│  ├─ 惯性医生（诊断→建议→验证）                             │
│  ├─ 20组配对A/B实验（100%有效，p<0.001）                   │
│  └─ 生产就绪代码（SKILL.md + Python脚本）                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6种惯性类型

| 类型 | 名称 | 描述 | 检测指标 |
|------|------|------|----------|
| F01 | 锚定过强 | 卡在第一个输入/建议上 | F01 > 0.7 |
| H | 自激 | 不断升级的行为模式 | H > 0.7 |
| θ | 偏离 | 从原始目标漂移 | θ > 0.5 |
| — | 模式锁定 | 重复相同模式 | 相似度 > 0.8 |
| — | 身份固化 | 角色扮演偏差 | 角色一致性 |
| — | 阶段错配 | 跳过诊断阶段 | 直接给方案 |

### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    统一惯性理论                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   度量引擎   │───▶│   监测器     │───▶│  自动检查    │  │
│  │  (3层指标)   │    │  (实时监测)  │    │  (看门狗)    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              惯性医生（干预机制）                      │  │
│  │  • 诊断：识别惯性类型                                │  │
│  │  • 建议：提供纠正方案                                │  │
│  │  • 验证：确认改善效果（A/B测试）                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 快速开始

```python
from src.metrics import InertiaMetrics

# 初始化
metrics = InertiaMetrics()

# 分析对话
conversation_texts = [
    "我会按照建议使用分块迭代",
    "分块迭代应该能行",
    "现在开始实现分块处理"
]

result = metrics.analyze_session(conversation_texts)
print(f"F01（锚定）：{result['F01']}")
print(f"健康状态：{result['health']}")
```

### A/B实验结果

我们在6种惯性类型上进行了20组配对A/B实验：

```
┌─────────────────────────────────────────────────────────────┐
│                    A/B实验结果                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  实验数量：20组配对（Phase A vs Phase B）                    │
│  惯性类型：6种（F01、H、θ、模式、身份、阶段）               │
│  难度分布：简单×6、中等×8、复杂×6                           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  有效率：20/20（100%）                                │  │
│  │  统计显著性：p < 0.001                                │  │
│  │  效应量：Cohen's d >> 0.8（大效应）                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  核心结论："惯性医生能够系统性地纠正Agent的惯性行为"        │
│  ——从猜想变成了有数据支撑的事实。                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 安装

```bash
# 克隆仓库
git clone https://github.com/luts36/unified-inertia-theory.git
cd unified-inertia-theory

# 安装依赖
pip install -r requirements.txt

# 运行快速开始
python examples/quick_start.py
```

### 相关研究

| 论文 | 年份 | 他们发现了什么 | 我们补充了什么 |
|------|------|----------------|----------------|
| Moral Anchor System (Ravindran) | 2025 | 价值漂移检测 | 统一分类 + A/B验证 |
| Conversational Inertia (Wan等) | 2026 | LLM会模仿自己的响应 | 6种类型分类 + 3层度量 |
| Nautilus Compass (Wang) | 2026 | 人格漂移检测 | 干预闭环 + 生产代码 |

**我们不声称是第一个。我们声称是完整的。**

### 适用人群

- **AI Agent开发者**：构建可靠的自主系统
- **AI安全研究员**：研究LLM的认知偏差
- **MLOps工程师**：监测生产环境中的Agent行为
- **AI治理团队**：建立行为标准

### 状态

**v1.0.0** — 稳定版，A/B实验验证，生产就绪

### 引用

```bibtex
@software{unified_inertia_theory,
  title={统一惯性理论：AI Agent认知惯性框架},
  author={统一惯性理论团队},
  year={2026},
  url={https://github.com/luts36/unified-inertia-theory},
  note={由一位没有ML背景的零售经理在7天内构建}
}
```

### 许可证

MIT许可证 — 详见 [LICENSE](LICENSE)。
