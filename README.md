# Unified Inertia Theory 统一惯性理论

[English](#english) | [中文](#中文)

---

## English

### What is this?

**The first complete framework for detecting, measuring, and correcting AI Agent cognitive inertia.**

AI Agents exhibit predictable behavioral patterns called "inertia" — they get stuck in anchoring, self-excitation, and other cognitive biases that degrade their performance. This framework provides:

- **6 types** of cognitive inertia with precise definitions
- **3-layer metrics** (F01 + H + θ) for quantitative measurement
- **A/B validated** intervention (20/20 experiments, p<0.001)
- **Production-ready** monitoring and auto-correction tools

### Why does this matter?

```
┌─────────────────────────────────────────────────────────────┐
│  Problem: AI Agents have cognitive inertia                  │
│                                                             │
│  • Anchoring: Stuck on first suggestion (85% of sessions)   │
│  • Self-excitation: Escalating patterns (H > 0.7)           │
│  • Deviation: Lost focus from original goal (θ > 0.5)       │
│                                                             │
│  Impact: Degraded output quality, wasted compute,           │
│          unreliable agent behavior                          │
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

### Comparison with Existing Research

| Aspect | Academic Papers | This Framework |
|--------|----------------|----------------|
| Concept | Scattered studies on "anchoring" | Unified 6-type classification |
| Measurement | No systematic metrics | 3-layer (F01+H+θ) with 7 rules |
| Intervention | Technical (latent steering) | Text-based advice (Inertia Doctor) |
| Validation | Single-group experiments | 20 paired A/B experiments (p<0.001) |
| Engineering | Papers only | Production-ready code |

### Who is this for?

- **AI Agent developers** building reliable autonomous systems
- **AI safety researchers** studying cognitive biases in LLMs
- **MLOps engineers** monitoring agent behavior in production
- **AI governance teams** establishing behavioral standards

### Status

**v1.0.0** — Stable, A/B validated, production-ready

### Citation

If you use this framework in your research, please cite:

```bibtex
@software{unified_inertia_theory,
  title={Unified Inertia Theory: A Framework for AI Agent Cognitive Inertia},
  author={Unified Inertia Theory Team},
  year={2026},
  url={https://github.com/luts36/unified-inertia-theory}
}
```

### License

MIT License — see [LICENSE](LICENSE) for details.

---

## 中文

### 这是什么？

**全球首个完整的AI Agent认知惯性检测、度量和纠正框架。**

AI Agent会表现出可预测的行为模式，称为"惯性"——它们会陷入锚定、自激等认知偏差，导致性能下降。本框架提供：

- **6种**认知惯性类型的精确定义
- **3层度量指标**（F01 + H + θ）进行量化测量
- **A/B实验验证**的干预方法（20组配对实验，p<0.001）
- **生产就绪**的监测和自动纠正工具

### 为什么这很重要？

```
┌─────────────────────────────────────────────────────────────┐
│  问题：AI Agent存在认知惯性                                  │
│                                                             │
│  • 锚定效应：卡在第一个建议上（85%的会话）                   │
│  • 自激模式：不断升级的行为模式（H > 0.7）                   │
│  • 偏离目标：从原始目标漂移（θ > 0.5）                       │
│                                                             │
│  影响：输出质量下降、计算资源浪费、Agent行为不可靠           │
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

### 项目结构

```
unified-inertia-theory/
├── README.md                 # 本文件
├── LICENSE                   # MIT许可证
├── requirements.txt          # Python依赖
├── src/
│   ├── __init__.py          # 包初始化
│   ├── metrics.py           # 3层惯性度量引擎
│   ├── monitor.py           # 实时惯性监测
│   ├── auto_check.py        # 自动健康检查
│   └── collapse.py          # 惯性模式分析
├── docs/
│   ├── theory.md            # 统一惯性理论文档
│   ├── ab-experiment-results.md    # A/B实验结果
│   ├── ab-experiment-methodology.md # 实验设计
│   └── ab-experiment-statistical.md # 统计方法
├── references/
│   ├── constraint-topology.md      # 约束拓扑方法论
│   ├── seven-directions.md         # 七方向干预方法
│   └── hidden-cue-design-guide.md  # 隐蔽线索设计指南
└── examples/
    └── quick_start.py       # 快速开始示例
```

### 与现有研究的对比

| 维度 | 学术论文 | 本框架 |
|------|----------|--------|
| 概念 | 零散研究"锚定效应" | 统一6种类型分类 |
| 度量 | 无系统度量 | 3层指标（F01+H+θ）+ 7条规则 |
| 干预 | 技术手段（latent steering） | 文本建议（惯性医生） |
| 验证 | 单组实验 | 20组配对A/B实验（p<0.001） |
| 工程化 | 仅论文 | 生产就绪代码 |

### 适用人群

- **AI Agent开发者**：构建可靠的自主系统
- **AI安全研究员**：研究LLM的认知偏差
- **MLOps工程师**：监测生产环境中的Agent行为
- **AI治理团队**：建立行为标准

### 状态

**v1.0.0** — 稳定版，A/B实验验证，生产就绪

### 引用

如果您在研究中使用本框架，请引用：

```bibtex
@software{unified_inertia_theory,
  title={统一惯性理论：AI Agent认知惯性框架},
  author={统一惯性理论团队},
  year={2026},
  url={https://github.com/luts36/unified-inertia-theory}
}
```

### 许可证

MIT许可证 — 详见 [LICENSE](LICENSE)。
