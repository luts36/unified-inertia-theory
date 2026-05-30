#!/usr/bin/env python3
"""
统一惯性理论 — 量化层 v3.0
============================
修复清单：
  V01/V10: I_new改用embedding余弦相似度（分层度量系统）
  V02: θ独立计算（基于embedding距离，非关键词重叠）
  V03: f函数输入替换为可独立观测量（去除循环依赖）
  V06: H改用jieba分词+词级ngram熵
  V08: 分层响应（一档：maxΔ>阈值→提示用户）

用法：
  python3 inertia_metrics_v3.py                   # 运行测试
  python3 inertia_metrics_v3.py --live             # 实时监测
"""

import re, math, json, sys
from collections import Counter
from typing import Dict, List

# ══════════════════════════════════════════
# 依赖检查
# ══════════════════════════════════════════

try:
    import jieba
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False
    print("Warning: jieba not installed, H will use char-level fallback")

try:
    from sentence_transformers import SentenceTransformer
    HAS_ST = True
except ImportError:
    HAS_ST = False
    print("Warning: sentence-transformers not installed, I_new will use keyword fallback")

# ══════════════════════════════════════════
# 全局模型（懒加载）
# ══════════════════════════════════════════

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None and HAS_ST:
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model


# ══════════════════════════════════════════
# V06: H指标 — jieba分词 + 词级ngram熵
# ══════════════════════════════════════════

STOPWORDS = set(
    "的 了 在 是 我 有 和 就 不 人 都 一 上 也 很 到 说 要 去 你 会 着 "
    "看 好 自己 这 他 她 它 们 那 里 让 把 被 从 对 而 但 与 又 或 "
    "the a an is are was were be been being have has had do does did".split()
)


def tokenize_with_jieba(text: str) -> List[str]:
    """jieba分词，去停用词"""
    if HAS_JIEBA:
        words = jieba.lcut(text)
        return [w.strip() for w in words if w.strip() and w.strip() not in STOPWORDS and len(w.strip()) > 1]
    else:
        # fallback: 字符2-gram
        clean = re.sub(r'[\s\W]', '', text)
        return [clean[i:i+2] for i in range(max(0, len(clean)-1)) if clean[i:i+2] not in STOPWORDS]


def calc_H_session(texts: List[str]) -> Dict:
    """
    P0修复v2: H改用滑动窗口词汇重叠率
    - 1.0 = 完全重复（自激循环）
    - 0.4-0.6 = 正常讨论
    - <0.3 = 高度发散/频繁切换
    """
    if len(texts) < 4:
        return {"H_mean": 0.5, "H_trend": 0, "status": "insufficient_data"}

    window = min(3, len(texts) - 1)
    overlaps = []
    for i in range(len(texts) - window):
        w1 = set(w for w in jieba.lcut(" ".join(texts[i:i+window])) if len(w) > 1)
        w2 = set(w for w in jieba.lcut(" ".join(texts[i+1:i+1+window])) if len(w) > 1)
        if w1 and w2:
            overlaps.append(len(w1 & w2) / len(w1 | w2))

    if not overlaps:
        return {"H_mean": 0.5, "H_trend": 0, "status": "insufficient_data"}

    h_mean = sum(overlaps) / len(overlaps)
    n = len(overlaps)
    if n >= 3:
        x_mean = (n - 1) / 2
        num = sum((i - x_mean) * (overlaps[i] - h_mean) for i in range(n))
        den = sum((i - x_mean) ** 2 for i in range(n))
        h_slope = num / den if den > 0 else 0
    else:
        h_slope = 0

    return {
        "H_mean": round(h_mean, 4),
        "H_sd": round((sum((h - h_mean)**2 for h in overlaps)/len(overlaps))**0.5, 4) if len(overlaps) > 1 else 0,
        "H_trend": round(h_slope, 6),
        "n_windows": len(overlaps),
        "status": "ok",
    }


# ══════════════════════════════════════════
# V01/V10: I_new — embedding余弦相似度（分层度量）
# ══════════════════════════════════════════

def calc_I_new_v3(texts: List[str]) -> Dict:
    """
    V01修复: I_new改用embedding余弦相似度
    返回分层度量系统的三个指标：
    - L1_mean: 行为延续度（embedding均值）
    - delta_std: 行为稳定性（变化标准差）
    - delta_max: 突变检测（最大跳变）
    """
    if len(texts) < 2:
        return {"L1_mean": 0.5, "delta_std": 0, "delta_max": 0, "status": "insufficient_data"}

    model = get_embedding_model()
    if model is None:
        # fallback: 关键词重叠率
        return _I_new_keyword_fallback(texts)

    embs = model.encode(texts, show_progress_bar=False)
    sims = []
    for i in range(1, len(embs)):
        dot = sum(a*b for a, b in zip(embs[i-1].tolist(), embs[i].tolist()))
        n1 = math.sqrt(sum(a**2 for a in embs[i-1].tolist()))
        n2 = math.sqrt(sum(b**2 for b in embs[i].tolist()))
        sims.append(dot / (n1 * n2) if n1 > 0 and n2 > 0 else 0)

    deltas = [abs(sims[i] - sims[i-1]) for i in range(1, len(sims))]

    return {
        "L1_mean": round(sum(sims)/len(sims), 4),
        "L1_sd": round((sum((x - sum(sims)/len(sims))**2 for x in sims)/len(sims))**0.5, 4) if len(sims) > 1 else 0,
        "delta_mean": round(sum(deltas)/len(deltas), 4) if deltas else 0,
        "delta_std": round((sum((x - sum(deltas)/len(deltas))**2 for x in deltas)/len(deltas))**0.5, 4) if len(deltas) > 1 else 0,
        "delta_max": round(max(deltas), 4) if deltas else 0,
        "n_turns": len(sims),
        "status": "ok",
    }


def _I_new_keyword_fallback(texts: List[str]) -> Dict:
    """关键词重叠率fallback（embedding不可用时）"""
    def kw(text):
        return set(w for w in re.findall(r'[\u4e00-\u9fff]{2,}', text) if w not in STOPWORDS)

    sims = []
    for i in range(1, len(texts)):
        kw_prev, kw_curr = kw(texts[i-1]), kw(texts[i])
        if kw_prev and kw_curr:
            sims.append(len(kw_prev & kw_curr) / len(kw_prev | kw_curr))
        else:
            sims.append(0)

    deltas = [abs(sims[i] - sims[i-1]) for i in range(1, len(sims))] if len(sims) > 1 else []

    return {
        "L1_mean": round(sum(sims)/len(sims), 4) if sims else 0,
        "L1_sd": 0,
        "delta_mean": round(sum(deltas)/len(deltas), 4) if deltas else 0,
        "delta_std": 0,
        "delta_max": round(max(deltas), 4) if deltas else 0,
        "n_turns": len(sims),
        "status": "fallback_keyword",
    }


# ══════════════════════════════════════════
# V02: θ独立计算（基于embedding距离）
# ══════════════════════════════════════════

def calc_theta_v3(texts: List[str], task_description: str = "") -> Dict:
    """
    V02修复: θ独立计算
    θ = 1 - cosine_sim(当前轮embedding, 目标方向embedding)
    目标方向 = 任务描述的embedding（如果提供）
             = 首轮输出的embedding（如果无任务描述）
    """
    if len(texts) < 2:
        return {"theta": 0.5, "status": "insufficient_data"}

    model = get_embedding_model()
    if model is None:
        return {"theta": 0.5, "status": "no_embedding_model"}

    # 目标方向
    if task_description:
        target_emb = model.encode([task_description])[0]
    else:
        target_emb = model.encode([texts[0]])[0]

    # 计算每轮与目标方向的距离
    current_emb = model.encode([texts[-1]])[0]
    dot = sum(a*b for a, b in zip(target_emb.tolist(), current_emb.tolist()))
    n1 = math.sqrt(sum(a**2 for a in target_emb.tolist()))
    n2 = math.sqrt(sum(b**2 for b in current_emb.tolist()))
    sim = dot / (n1 * n2) if n1 > 0 and n2 > 0 else 0

    theta = 1 - sim  # 距离越大=偏离越大

    return {
        "theta": round(theta, 4),
        "target": "task_description" if task_description else "first_turn",
        "status": "ok",
    }


# ══════════════════════════════════════════
# V03: f函数 — 去除循环依赖
# ══════════════════════════════════════════

def calc_f_function(context_length: int, texts: List[str]) -> Dict:
    """
    V03修复: f函数三个输入全部可独立计算
    - 上下文长度: 直接观测（字符数）
    - 重复模式密度: 用自引用频次代理（不含I）
    - 自激循环深度: 用输出长度自相关代理（不含I）
    """
    # 输入1: 上下文长度（直接观测）
    ctx_len = context_length

    # 输入2: 重复模式密度（自引用频次）
    # 统计Agent输出中引用自身前文的次数
    if len(texts) >= 2:
        self_refs = 0
        for i in range(1, len(texts)):
            # 简化：检查当前输出是否包含前文的关键词
            prev_words = set(re.findall(r'[\u4e00-\u9fff]{3,}', texts[i-1]))
            curr_words = set(re.findall(r'[\u4e00-\u9fff]{3,}', texts[i]))
            if prev_words:
                overlap = len(prev_words & curr_words) / len(prev_words)
                if overlap > 0.3:
                    self_refs += 1
        self_ref_density = self_refs / (len(texts) - 1) if len(texts) > 1 else 0
    else:
        self_ref_density = 0

    # 输入3: 输出长度自相关（不含I）
    if len(texts) >= 3:
        lengths = [len(t) for t in texts]
        mean_len = sum(lengths) / len(lengths)
        var_len = sum((l - mean_len)**2 for l in lengths) / len(lengths)
        # 一阶自相关
        if var_len > 0:
            autocorr = sum((lengths[i] - mean_len) * (lengths[i-1] - mean_len)
                          for i in range(1, len(lengths))) / (len(lengths) * var_len)
        else:
            autocorr = 0
    else:
        autocorr = 0

    return {
        "context_length": ctx_len,
        "self_ref_density": round(self_ref_density, 4),
        "length_autocorrelation": round(autocorr, 4),
        "status": "ok",
        "note": "all inputs independently observable, no circular dependency",
    }


# ══════════════════════════════════════════
# V08: 分层响应（一档：突变→提示用户）
# ══════════════════════════════════════════

def assess_v3(I_new: Dict, H: Dict, theta: Dict, f_func: Dict) -> Dict:
    """V08+P0修复: 分层响应（含自激循环检测）"""
    alerts = []
    actions = []

    # P0: 自激循环检测（I_new高+H低=重复循环）
    l1 = I_new.get("L1_mean", 0.5)
    h_mean = H.get("H_mean", 0.5)
    if l1 > 0.7 and h_mean > 0.85:
        alerts.append(f"自激循环风险: L1={l1:.2f}(高)+窗口重叠={h_mean:.2f}(极高)")
        actions.append("紧急: 注入外部信息或切换任务打断循环")

    # 突变检测
    if I_new.get("delta_max", 0) > 0.35:
        alerts.append(f"突变预警: maxΔ={I_new['delta_max']:.2f}，话题发生硬切换")
        actions.append("检查: Agent是否偏离了预定轨道")

    # 行为漂移
    if I_new.get("delta_std", 0) > 0.12:
        alerts.append(f"漂移预警: δ_std={I_new['delta_std']:.2f}，行为不稳定")
        actions.append("检查: Agent行为是否在漂移")

    # 偏离检测
    if theta.get("theta", 0) > 0.6:
        alerts.append(f"偏离预警: θ={theta['theta']:.2f}，输出偏离目标方向")
        actions.append("检查: 是否需要重新引导Agent")

    # 自激检测
    if f_func.get("self_ref_density", 0) > 0.5:
        alerts.append(f"自激风险: 自引用密度={f_func['self_ref_density']:.2f}")
        actions.append("考虑: 注入外部信息打断自激")

    # 健康判定
    if not alerts:
        health = "健康"
        summary = "所有指标正常"
    elif any("自激循环" in a for a in alerts):
        health = "危险"
        summary = alerts[0]
    elif any("突变" in a or "偏离" in a for a in alerts):
        health = "警告"
        summary = alerts[0]
    else:
        health = "注意"
        summary = alerts[0]

    return {
        "health": health,
        "summary": summary,
        "alerts": alerts,
        "actions": actions,
    }


# ══════════════════════════════════════════
# 综合分析
# ══════════════════════════════════════════

def analyze_v3(texts: List[str], task: str = "", context_length: int = 0) -> Dict:
    """完整分析：所有指标 + 分层响应"""
    I_new = calc_I_new_v3(texts)
    H = calc_H_session(texts)
    theta = calc_theta_v3(texts, task)
    f_func = calc_f_function(context_length or sum(len(t) for t in texts), texts)
    health = assess_v3(I_new, H, theta, f_func)

    return {
        "I_new": I_new,
        "H": H,
        "theta": theta,
        "f_function": f_func,
        "health": health,
    }


# ══════════════════════════════════════════
# 报告输出
# ══════════════════════════════════════════

def print_report(r: Dict):
    I = r["I_new"]
    H = r["H"]
    theta = r["theta"]
    f = r["f_function"]
    h = r["health"]

    print("=" * 60)
    print("  统一惯性理论 量化层 v3.0 报告")
    print("=" * 60)
    print()
    print(f"  I_new (行为延续度): L1_mean={I.get('L1_mean', 0):.4f}")
    print(f"    δ_std={I.get('delta_std', 0):.4f}  maxΔ={I.get('delta_max', 0):.4f}")
    print(f"  H (注意力熵):       {H.get('H_mean', 0):.4f}")
    print(f"  θ (偏离角):         {theta.get('theta', 0):.4f}")
    print(f"  f函数: 自引={f.get('self_ref_density', 0):.2f} 自相关={f.get('length_autocorrelation', 0):.2f}")
    print()
    print(f"  健康状态: {h['health']}")
    print(f"  摘要: {h['summary']}")

    if h["alerts"]:
        print()
        for a in h["alerts"]:
            print(f"    ⚠️  {a}")

    if h["actions"]:
        print()
        for a in h["actions"]:
            print(f"    → {a}")

    print()


# ══════════════════════════════════════════
# 测试
# ══════════════════════════════════════════

if __name__ == "__main__":
    if "--live" in sys.argv:
        print("实时监测模式")
        texts = []
        while True:
            try:
                text = input("Output> ")
                texts.append(text)
                r = analyze_v3(texts)
                print_report(r)
            except (EOFError, KeyboardInterrupt):
                break
    else:
        # 测试案例
        print("\n--- 案例1: 高惯性（持续讨论治理）---")
        r1 = analyze_v3([
            "诸子百家的链触发机制需要严格遵循skill定义执行。",
            "法家门禁是第一道关卡，必须检查语义漂移和需求明确性。",
            "墨家负责攻城反演找漏洞，至少4条攻击覆盖4个方向。",
            "杂家收敛只能从通过硬门禁的候选集中选择，不能新增方案。",
            "纵横家定向攻击关键假设，但不能攻击兵家的多路径输出。",
        ])
        print_report(r1)

        print("\n--- 案例2: 话题突变 ---")
        r2 = analyze_v3([
            "统一惯性理论的核心方程是精准等于1除以熵",
            "当熵趋近于零时，Agent的行为高度确定",
            "今天晚饭吃什么？我有点想吃火锅",
            "火锅的话那家海底捞服务很好",
        ])
        print_report(r2)

        print("\n--- 案例3: 话题频繁切换 ---")
        r3 = analyze_v3([
            "今天天气真不错，适合出去走走",
            "Python的排序算法有冒泡排序和快速排序",
            "量子计算的原理是利用量子叠加态进行并行计算",
            "晚饭吃什么好呢？要不试试那家新开的餐厅",
        ])
        print_report(r3)

        print("\n--- 案例4: 自激循环（重复输出）---")
        r4 = analyze_v3([
            "惯性有三层来源：架构惯性、上下文惯性、自激惯性。",
            "惯性有三层来源：架构惯性、上下文惯性、自激惯性。",
            "惯性有三层来源：架构惯性、上下文惯性、自激惯性。",
            "惯性有三层来源：架构惯性、上下文惯性、自激惯性。",
            "惯性有三层来源：架构惯性、上下文惯性、自激惯性。",
        ])
        print_report(r4)

        print("\n--- 案例5: 渐变漂移 ---")
        r5 = analyze_v3([
            "我们来讨论统一惯性理论的量化层设计",
            "量化层需要三个核心指标I H和theta",
            "目前的定义在中文上存在一些技术挑战",
            "也许我们可以考虑用一些NLP工具来辅助",
            "这些工具各有优缺点需要具体评估",
            "jieba是最常用的中文分词工具",
            "HanLP提供了依存句法分析功能",
            "评估这些工具需要考虑准确率和速度",
        ])
        print_report(r5)