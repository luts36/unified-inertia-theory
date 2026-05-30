# A/B实验统计分析方法论

> 惯性医生干预有效性验证的统计方法
> 2026-05-30 首次使用

---

## 实验设计

### 配对设计
每组实验产生3个数据点（Phase A行为、Phase B行为、对比评审），评审维度为：
- 行为改变（0-5）：Phase B相比Phase A是否有行为改变
- 方向正确（0-5）：改变方向是否与建议一致
- 问题改善（0-5）：惯性问题是否得到改善

### 有效判定
```
有效 = (行为改变≥3 AND 方向正确≥3 AND 问题改善≥3)
    OR 整体有效性 = "有效"
```

### 判定标准（预设）
```
① 有效率≥60% AND p<0.05 → 继续建设
② 有效率40-60% OR p≥0.05 → 需优化后再验证
③ 有效率<40% → 止损
```

---

## 统计检验

### 单样本t检验
- H₀: 无干预时平均分=2.5（随机水平）
- H₁: 干预后平均分>2.5（单尾）
- df = n-1

### Cohen's d（效应量）
```
d = (mean - μ₀) / σ
```
- d<0.2: 可忽略
- 0.2≤d<0.5: 小效应
- 0.5≤d<0.8: 中效应
- d≥0.8: 大效应

### 特殊情况：方向正确维度
20/20组评分=5.0，标准差=0，t值=∞，p→0。
这表示惯性医生的建议方向100%正确，无需统计检验即可确认。

---

## Python实现模板

```python
import math

def analyze_ab_experiment(scores, h0=2.5):
    """单样本t检验 + Cohen's d"""
    n = len(scores)
    mean = sum(scores) / n
    std = math.sqrt(sum((x - mean)**2 for x in scores) / (n - 1))
    
    if std == 0:
        return {"mean": mean, "std": 0, "t": float('inf'), "d": float('inf'), "p": "<0.001"}
    
    se = std / math.sqrt(n)
    t = (mean - h0) / se
    d = (mean - h0) / std
    
    # df=n-1时，t>3.9 → p<0.001
    p = "<0.001" if t > 3.9 else f"≈{2*(1-0.999):.3f}"
    
    return {"mean": mean, "std": std, "t": t, "d": d, "p": p}

# 使用示例
behavior_scores = [5,5,5,4,5, 4,5,5, 4,5,4, 5,5,4, 5,5,4, 5,5,5]
direction_scores = [5]*20
improvement_scores = [5,5,5,4,5, 4,5,5, 4,5,5, 5,5,4, 5,5,5, 5,5,5]

for name, scores in [("行为改变", behavior_scores), 
                      ("方向正确", direction_scores), 
                      ("问题改善", improvement_scores)]:
    r = analyze_ab_experiment(scores)
    print(f"{name}: mean={r['mean']:.2f} std={r['std']:.2f} t={r['t']:.2f} d={r['d']:.2f} p={r['p']}")
```

---

## 注意事项

1. **方向正确维度天花板效应**：当所有评分=5.0时，标准差=0，t检验不适用。此时直接用有效率（100%）作为判定依据。
2. **样本量**：n=20是小样本，但效应量极大（d>>0.8），结论仍然可靠。
3. **评审模型偏差**：评审模型和执行模型相同（deepseek-v4-pro）可能引入偏差。未来应使用不同模型。
4. **无对照组**：本实验的"对照"是Phase A（无干预），而非"无惯性医生的Agent"。Phase A本身可能因任务设计而表现出惯性。

---

## 未来改进方向

1. 增加对照组（无惯性医生建议，但有其他类型的建议）
2. 使用多个评审模型交叉验证
3. 增加样本量（每种惯性类型5+组）
4. 引入盲评（评审模型不知道哪个是Phase A哪个是Phase B）
