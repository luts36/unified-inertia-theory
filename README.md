# Unified Inertia Theory 统一惯性理论

[English](#english) | [中文](#中文)

---

## English

### What is this?

**The first engineering-complete framework for detecting, measuring, and correcting AI Agent cognitive inertia.**

27 days from zero to open source. No research team. No academic background. No references. Pure self-exploration from daily Agent usage.

### The Story

> **How I built this**

I started using AI Agents in May 2026.

Within weeks, I noticed something: my Agent kept repeating the same mistakes. It would anchor on the first suggestion, escalate patterns in conversations, and drift away from goals.

I had never read a paper about "cognitive bias in LLMs." I didn't know the term "anchoring effect." I just knew something was wrong.

So I started observing. And building. And testing.

I called the phenomenon "inertia" — borrowing from physics. I built a measurement system from scratch. I created a diagnostic tool. I designed 20 A/B experiments to validate it.

**No references. No team. No budget. Just a user who refused to accept "that's just how AI works."**

### Why This Matters

```
┌─────────────────────────────────────────────────────────────┐
│  The Gap in AI Agent Research                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Academic Papers (2025-2026)                                │
│  ├─ Found "conversational inertia" exists                   │
│  ├─ Found "persona drift" can be detected                   │
│  └─ Published papers with theoretical frameworks            │
│                                                             │
│  What They Didn't Do                                        │
│  ├─ Build a complete classification system                  │
│  ├─ Create production-ready measurement tools               │
│  ├─ Design an intervention loop                             │
│  ├─ Validate with 20 paired A/B experiments                 │
│  └─ Release working code                                    │
│                                                             │
│  What I Built                                               │
│  ├─ 6-type classification (from observation, not papers)    │
│  ├─ 3-layer metrics (F01 + H + θ, from scratch)            │
│  ├─ Inertia Doctor (diagnose → advise → verify)             │
│  ├─ 20 paired A/B experiments (100% effective, p<0.001)     │
│  └─ Production-ready code (tested on 586+ sessions)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### The Difference

**Academic approach**: Read papers → Find gap → Design experiment → Publish paper

**My approach**: Use Agent → Notice problem → Observe patterns → Build solution → Test it → Release it

I didn't start from literature. I started from practice.

That's why this framework is different. It's built by a user, for users.

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

**We didn't reference any of these. We discovered independently.**

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
  note={Built in 27 days, from zero, with no references}
}
```

### License

MIT License — see [LICENSE](LICENSE) for details.

---

## 中文

### 这是什么？

**首个工程完整的AI Agent认知惯性检测、度量和纠正框架。**

27天从零到开源。没有研究团队。没有学术背景。没有参考文献。纯粹从日常Agent使用中自我摸索。

### 故事

> **我是怎么做到的**

2026年5月，我开始使用AI Agent。

几周内，我发现了一个问题：我的Agent一直在重复同样的错误。它会卡在第一个建议上，在对话中不断升级模式，从目标漂移。

我从来没读过关于"LLM认知偏差"的论文。我不知道"锚定效应"这个术语。我只知道有什么不对劲。

于是我开始观察。开始构建。开始测试。

我把这种现象叫做"惯性"——借用物理学的概念。我从零构建了度量系统。我创建了诊断工具。我设计了20组A/B实验来验证它。

**没有参考文献。没有团队。没有经费。只是一个拒绝接受"AI就是这样"的用户。**

### 为什么这很重要

```
┌─────────────────────────────────────────────────────────────┐
│  AI Agent研究的空白                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  学术论文（2025-2026）                                      │
│  ├─ 发现"会话惯性"存在                                      │
│  ├─ 发现"人格漂移"可以被检测                                │
│  └─ 发表了理论框架的论文                                    │
│                                                             │
│  他们没做到的                                               │
│  ├─ 构建完整的分类系统                                      │
│  ├─ 创建生产就绪的度量工具                                  │
│  ├─ 设计干预闭环                                            │
│  ├─ 用20组配对A/B实验验证                                   │
│  └─ 发布可用的代码                                          │
│                                                             │
│  我做到的                                                   │
│  ├─ 6种类型分类（从观察中发现，不是从论文中学习）           │
│  ├─ 3层度量指标（F01 + H + θ，从零构建）                   │
│  ├─ 惯性医生（诊断→建议→验证）                             │
│  ├─ 20组配对A/B实验（100%有效，p<0.001）                   │
│  └─ 生产就绪代码（在586+个session上测试）                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 区别

**学术路径**：读论文 → 找空白 → 设计实验 → 发表论文

**我的路径**：用Agent → 发现问题 → 观察模式 → 构建方案 → 测试 → 发布

我不是从文献开始的。我是从实践开始的。

这就是为什么这个框架不同。它是由用户构建的，为用户服务。

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

**我们没有参考任何这些。我们是独立发现的。**

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
  note={27天从零构建，无参考，纯自我摸索}
}
```

### 许可证

MIT许可证 — 详见 [LICENSE](LICENSE)。
