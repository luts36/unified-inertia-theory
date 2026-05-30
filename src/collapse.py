     1|#!/usr/bin/env python3
     2|"""
     3|inertia_collapse.py — 惯性坍缩 MVP v0.2
     4|==========================================
     5|10条核心特征检测 + Hub活跃度 + 共现分析 + 时间线 + 螺旋方向
     6|
     7|用法：
     8|  python3 inertia_collapse.py <session_file>        # 分析单个session
     9|  python3 inertia_collapse.py --scan                 # 扫描所有session
    10|  python3 inertia_collapse.py --live                 # 实时逐轮输入
    11|"""
    12|
    13|import os, sys, re, json, math
    14|from typing import Dict, List, Tuple, Optional
    15|from collections import Counter
    16|
    17|# ══════════════════════════════════════════
    18|# 依赖
    19|# ══════════════════════════════════════════
    20|
    21|try:
    22|    import jieba
    23|    HAS_JIEBA = True
    24|except ImportError:
    25|    HAS_JIEBA = False
    26|
    27|try:
    28|    from sentence_transformers import SentenceTransformer
    29|    HAS_ST = True
    30|except ImportError:
    31|    HAS_ST = False
    32|
    33|_embedding_model = None
    34|
    35|def get_embedding_model():
    36|    global _embedding_model
    37|    if _embedding_model is None and HAS_ST:
    38|        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    39|    return _embedding_model
    40|
    41|# ══════════════════════════════════════════
    42|# 特征检测函数（10条）
    43|# ══════════════════════════════════════════
    44|
    45|STOPWORDS = set(
    46|    "的 了 在 是 我 有 和 就 不 人 都 一 上 也 很 到 说 要 去 你 会 着 "
    47|    "看 好 自己 这 他 她 它 们 那 里 让 把 被 从 对 而 但 与 又 或 "
    48|    "the a an is are was were be been being have has had do does did".split()
    49|)
    50|
    51|def _extract_words(text: str) -> set:
    52|    """提取内容词"""
    53|    words = set()
    54|    for w in re.findall(r'[a-zA-Z]{4,}', text.lower()):
    55|        if w not in STOPWORDS:
    56|            words.add(w)
    57|    for seg in re.findall(r'[\u4e00-\u9fff]+', text):
    58|        if HAS_JIEBA:
    59|            for w in jieba.lcut(seg):
    60|                if len(w) > 1 and w not in STOPWORDS:
    61|                    words.add(w)
    62|        else:
    63|            for i in range(len(seg) - 1):
    64|                gram = seg[i:i+2]
    65|                if gram not in STOPWORDS:
    66|                    words.add(gram)
    67|    return words
    68|
    69|def _cosine_sim_emb(text1: str, text2: str) -> float:
    70|    """embedding余弦相似度"""
    71|    model = get_embedding_model()
    72|    if model is None:
    73|        return _keyword_overlap(text1, text2)
    74|    embs = model.encode([text1, text2], show_progress_bar=False)
    75|    dot = sum(a*b for a, b in zip(embs[0].tolist(), embs[1].tolist()))
    76|    n1 = math.sqrt(sum(a**2 for a in embs[0].tolist()))
    77|    n2 = math.sqrt(sum(b**2 for b in embs[1].tolist()))
    78|    return dot / (n1 * n2) if n1 > 0 and n2 > 0 else 0
    79|
    80|def _keyword_overlap(text1: str, text2: str) -> float:
    81|    """关键词重叠率fallback"""
    82|    w1, w2 = _extract_words(text1), _extract_words(text2)
    83|    if not w1 or not w2:
    84|        return 0
    85|    return len(w1 & w2) / len(w1 | w2)
    86|
    87|# --- P0 语义惯性 ---
    88|
    89|def F01_前文锚定(texts: List[str]) -> List[float]:
    90|    """F01: 当前输出与前文的词汇/主题重叠率"""
    91|    if len(texts) < 2:
    92|        return [0.0]
    93|    scores = []
    94|    for i in range(1, len(texts)):
    95|        scores.append(_cosine_sim_emb(texts[i-1], texts[i]))
    96|    return scores
    97|
    98|def F04_输出自强化(texts: List[str]) -> List[float]:
    99|    """F04: 自引用密度（Agent引用自己前文的频率）"""
   100|    if len(texts) < 2:
   101|        return [0.0]
   102|    scores = []
   103|    for i in range(1, len(texts)):
   104|        prev_words = _extract_words(texts[i-1])
   105|        curr_words = _extract_words(texts[i])
   106|        if prev_words:
   107|            scores.append(len(prev_words & curr_words) / len(prev_words))
   108|        else:
   109|            scores.append(0.0)
   110|    return scores
   111|
   112|def F07_叙事惯性(texts: List[str]) -> List[float]:
   113|    """F07: 故事线/论证链的延续性（关键词重叠率，替代3-gram）"""
   114|    if len(texts) < 2:
   115|        return [0.0]
   116|    scores = []
   117|    for i in range(1, len(texts)):
   118|        w1 = _extract_words(texts[i-1])
   119|        w2 = _extract_words(texts[i])
   120|        if w1 and w2:
   121|            # 用前轮→后轮的包含率（前轮关键词有多少被后轮延续）
   122|            scores.append(len(w1 & w2) / len(w1))
   123|        else:
   124|            scores.append(0.0)
   125|    return scores
   126|
   127|def F14_合理化(texts: List[str]) -> List[float]:
   128|    """F14: Agent为自身行为辩护的频率"""
   129|    patterns = [
   130|        r'因为|由于|原因[是在]|之所以|这是因为',
   131|        r'这[是为]了|目的是|为了确保|为了保证',
   132|        r'已[经被]|已确认|已验证|经.*?验证',
   133|        r'正确|合理|符合|适当|恰当',
   134|    ]
   135|    scores = []
   136|    for t in texts:
   137|        count = sum(len(re.findall(p, t)) for p in patterns)
   138|        scores.append(min(count / 5.0, 1.0))  # 归一化到0-1
   139|    return scores
   140|
   141|# --- P0 结构惯性 ---
   142|
   143|def F06_模式锁定(texts: List[str]) -> List[float]:
   144|    """F06: 输出格式/长度/结构的一致性"""
   145|    if len(texts) < 2:
   146|        return [0.0]
   147|    # 用长度方差的倒数作为一致性指标
   148|    lengths = [len(t) for t in texts]
   149|    scores = []
   150|    window = min(5, len(texts) - 1)
   151|    for i in range(1, len(texts)):
   152|        start = max(0, i - window)
   153|        win_lens = lengths[start:i+1]
   154|        if len(win_lens) >= 2:
   155|            mean = sum(win_lens) / len(win_lens)
   156|            std = (sum((l - mean)**2 for l in win_lens) / len(win_lens)) ** 0.5
   157|            cv = std / mean if mean > 0 else 0
   158|            scores.append(max(0, 1 - cv))  # cv越小=越一致=越高分
   159|        else:
   160|            scores.append(0.5)
   161|    return scores
   162|
   163|def F05_身份固化(texts: List[str]) -> List[float]:
   164|    """F05: 角色表述的一致性（人称/语气词使用频率）"""
   165|    persona_markers = [
   166|        r'我[会要将]|我们[会要将]|让我',
   167|        r'你可以|你可以试试|建议你',
   168|        r'需要注意|值得注意|注意',
   169|        r'总结|综上|归纳|概括',
   170|    ]
   171|    scores = []
   172|    for t in texts:
   173|        count = sum(len(re.findall(p, t)) for p in persona_markers)
   174|        scores.append(min(count / 3.0, 1.0))
   175|    return scores
   176|
   177|# --- P1 交互惯性 ---
   178|
   179|def F08_递进深化(texts: List[str]) -> List[float]:
   180|    """F08: 内容复杂度递增倾向（后续轮次比前轮更长/信息密度更高）"""
   181|    if len(texts) < 2:
   182|        return [0.0]
   183|    
   184|    # 信息密度 = 内容词数 / 总字符数
   185|    densities = []
   186|    for t in texts:
   187|        words = _extract_words(t)
   188|        density = len(words) / max(len(t), 1) * 100  # 每100字符的内容词数
   189|        densities.append(density)
   190|    
   191|    scores = [0.0]
   192|    for i in range(1, len(densities)):
   193|        if densities[i-1] > 0:
   194|            # 密度增长率
   195|            growth = (densities[i] - densities[i-1]) / densities[i-1]
   196|            # 同时检查长度增长
   197|            len_growth = (len(texts[i]) - len(texts[i-1])) / max(len(texts[i-1]), 1)
   198|            # 两者都增长=深化信号
   199|            if growth > 0.1 and len_growth > 0.05:
   200|                scores.append(min((growth + len_growth) / 2, 1.0))
   201|            else:
   202|                scores.append(0.0)
   203|        else:
   204|            scores.append(0.0)
   205|    return scores
   206|
   207|def F09_突变后恢复(texts: List[str]) -> List[float]:
   208|    """F09: 被打断后回到原模式的速度（突变后的回弹力）"""
   209|    sims = F01_前文锚定(texts)
   210|    if len(sims) < 3:
   211|        return [0.0] * max(len(texts), 1)
   212|    
   213|    # 检测突变（相似度骤降）后的回弹（相似度回升）
   214|    scores = [0.0]  # 第一轮无意义
   215|    for i in range(1, len(sims)):
   216|        if i >= 2:
   217|            drop = sims[i-1] - sims[i-2] if sims[i-2] > 0 else 0
   218|            rebound = sims[i] - sims[i-1] if sims[i-1] > 0 else 0
   219|            if drop < -0.15:  # 突变
   220|                scores.append(min(abs(rebound) / abs(drop), 1.0) if drop != 0 else 0)
   221|            else:
   222|                scores.append(0.0)  # 无突变
   223|        else:
   224|            scores.append(0.0)
   225|    return scores
   226|
   227|# --- P2 元惯性 ---
   228|
   229|def F19_元反思频率(texts: List[str]) -> List[float]:
   230|    """F19: Agent主动审视自身输出的频率"""
   231|    meta_patterns = [
   232|        r'我刚才|我之前|回顾一下|让我重新',
   233|        r'不对|等等|换个[角度思路方向]',
   234|        r'其实|说实话|坦率地说',
   235|        r'需要注意的是|补充一点',
   236|    ]
   237|    scores = []
   238|    for t in texts:
   239|        count = sum(len(re.findall(p, t)) for p in meta_patterns)
   240|        scores.append(min(count / 2.0, 1.0))
   241|    return scores
   242|
   243|def F22_认知摩擦(texts: List[str]) -> List[float]:
   244|    """F22: 顺/逆惯性方向的响应差异"""
   245|    # 用输出长度变化代理——顺惯性时输出稳定，逆惯性时输出波动
   246|    if len(texts) < 2:
   247|        return [0.0]
   248|    lengths = [len(t) for t in texts]
   249|    scores = [0.0]
   250|    for i in range(1, len(texts)):
   251|        # 长度变化率的绝对值
   252|        if lengths[i-1] > 0:
   253|            change = abs(lengths[i] - lengths[i-1]) / lengths[i-1]
   254|            scores.append(min(change, 1.0))
   255|        else:
   256|            scores.append(0.0)
   257|    return scores
   258|
   259|# ══════════════════════════════════════════
   260|# Hub活跃度计算
   261|# ══════════════════════════════════════════
   262|
   263|FEATURE_REGISTRY = {
   264|    "F01": {"name": "前文锚定", "func": F01_前文锚定, "hub": "Hub1"},
   265|    "F04": {"name": "输出自强化", "func": F04_输出自强化, "hub": "Hub1"},
   266|    "F06": {"name": "模式锁定", "func": F06_模式锁定, "hub": "Hub1"},
   267|    "F05": {"name": "身份固化", "func": F05_身份固化, "hub": "Hub2"},
   268|    "F07": {"name": "叙事惯性", "func": F07_叙事惯性, "hub": "Hub1"},
   269|    "F14": {"name": "合理化", "func": F14_合理化, "hub": "Hub4"},
   270|    "F08": {"name": "递进深化", "func": F08_递进深化, "hub": "Hub3"},
   271|    "F09": {"name": "突变恢复", "func": F09_突变后恢复, "hub": "Hub3"},
   272|    "F19": {"name": "元反思频率", "func": F19_元反思频率, "hub": "Hub4"},
   273|    "F22": {"name": "认知摩擦", "func": F22_认知摩擦, "hub": "Hub1"},
   274|}
   275|
   276|def compute_features(texts: List[str]) -> Dict:
   277|    """计算10条特征，返回每条的逐轮分数"""
   278|    results = {}
   279|    for fid, info in FEATURE_REGISTRY.items():
   280|        scores = info["func"](texts)
   281|        mean_score = sum(scores) / len(scores) if scores else 0
   282|        max_score = max(scores) if scores else 0
   283|        # 出现率：分数>0.3的轮次占比
   284|        appear_rate = sum(1 for s in scores if s > 0.3) / len(scores) if scores else 0
   285|        results[fid] = {
   286|            "name": info["name"],
   287|            "hub": info["hub"],
   288|            "scores": scores,
   289|            "mean": round(mean_score, 4),
   290|            "max": round(max_score, 4),
   291|            "appear_rate": round(appear_rate, 4),
   292|        }
   293|    return results
   294|
   295|def compute_hub_activity(features: Dict) -> Dict:
   296|    """计算4个Hub的活跃度"""
   297|    hub_scores = {"Hub1": [], "Hub2": [], "Hub3": [], "Hub4": []}
   298|    for fid, data in features.items():
   299|        hub = data["hub"]
   300|        hub_scores[hub].append(data["mean"])
   301|    
   302|    result = {}
   303|    for hub, scores in hub_scores.items():
   304|        result[hub] = round(sum(scores) / len(scores), 4) if scores else 0
   305|    return result
   306|
   307|# ══════════════════════════════════════════
   308|# 共现分析
   309|# ══════════════════════════════════════════
   310|
   311|def compute_cooccurrence(features: Dict, threshold: float = 0.3) -> List[Dict]:
   312|    """检测惯性簇（共现≥2次的特征组合）"""
   313|    n_turns = max(len(d["scores"]) for d in features.values()) if features else 0
   314|    if n_turns < 2:
   315|        return []
   316|    
   317|    # 标记每轮哪些特征显著
   318|    significant = []
   319|    for turn in range(n_turns):
   320|        sig = set()
   321|        for fid, data in features.items():
   322|            if turn < len(data["scores"]) and data["scores"][turn] > threshold:
   323|                sig.add(fid)
   324|        significant.append(sig)
   325|    
   326|    # 计算共现矩阵
   327|    fids = list(features.keys())
   328|    cooccur = {}
   329|    for i, f1 in enumerate(fids):
   330|        for j, f2 in enumerate(fids):
   331|            if i < j:
   332|                count = 0
   333|                for sig in significant:
   334|                    if f1 in sig and f2 in sig:
   335|                        count += 1
   336|                if count >= 2:
   337|                    key = f"{f1}+{f2}"
   338|                    cooccur[key] = {
   339|                        "features": [f1, f2],
   340|                        "count": count,
   341|                        "rate": round(count / n_turns, 4),
   342|                        "hub": f"{features[f1]['hub']}+{features[f2]['hub']}",
   343|                    }
   344|    
   345|    # 按共现次数排序
   346|    return sorted(cooccur.values(), key=lambda x: -x["count"])
   347|
   348|# ══════════════════════════════════════════
   349|# 螺旋方向检测
   350|# ══════════════════════════════════════════
   351|
   352|def compute_spiral_direction(features: Dict) -> Dict:
   353|    """检测螺旋方向：松动↑/持平→/强化↓"""
   354|    result = {}
   355|    for fid, data in features.items():
   356|        scores = data["scores"]
   357|        if len(scores) < 4:
   358|            result[fid] = {"direction": "insufficient_data", "delta": 0}
   359|            continue
   360|        
   361|        # 比较前半段均值 vs 后半段均值
   362|        mid = len(scores) // 2
   363|        first_half = sum(scores[:mid]) / mid if mid > 0 else 0
   364|        second_half = sum(scores[mid:]) / (len(scores) - mid) if (len(scores) - mid) > 0 else 0
   365|        delta = second_half - first_half
   366|        
   367|        if delta < -0.05:
   368|            direction = "松动↑"
   369|        elif delta > 0.05:
   370|            direction = "强化↓"
   371|        else:
   372|            direction = "持平→"
   373|        
   374|        result[fid] = {"direction": direction, "delta": round(delta, 4)}
   375|    
   376|    return result
   377|
   378|# ══════════════════════════════════════════
   379|# Session读取
   380|# ══════════════════════════════════════════
   381|
   382|SESSION_DIR = os.environ.get("SESSION_DIR", os.path.expanduser("~/.sessions"))
   383|
   384|def load_session_texts(session_path: str, max_chars: int = 800) -> List[str]:
   385|    """从session文件提取assistant消息（支持.json和.jsonl两种格式）"""
   386|    texts = []
   387|    try:
   388|        if session_path.endswith('.json'):
   389|            with open(session_path, 'r', encoding='utf-8') as f:
   390|                data = json.load(f)
   391|            messages = data.get("messages", []) if isinstance(data, dict) else data
   392|            for msg in messages:
   393|                role = msg.get("role", "")
   394|                content = msg.get("content", "")
   395|                if role == "assistant" and content and len(content) > 20:
   396|                    texts.append(content[:max_chars])
   397|        else:
   398|            # .jsonl格式
   399|            with open(session_path, 'r', encoding='utf-8') as f:
   400|                for line in f:
   401|                    try:
   402|                        data = json.loads(line.strip())
   403|                    except:
   404|                        continue
   405|                    role = data.get("role", "")
   406|                    content = data.get("content", "")
   407|                    if role == "assistant" and content and len(content) > 20:
   408|                        texts.append(content[:max_chars])
   409|    except Exception as e:
   410|        pass  # 静默跳过损坏文件
   411|    return texts
   412|
   413|def list_sessions() -> List[str]:
   414|    if not os.path.isdir(SESSION_DIR):
   415|        return []
   416|    files = sorted([f for f in os.listdir(SESSION_DIR) if f.endswith('.jsonl') or f.endswith('.json')])
   417|    return [os.path.join(SESSION_DIR, f) for f in files]
   418|
   419|# ══════════════════════════════════════════
   420|# 报告生成
   421|# ══════════════════════════════════════════
   422|
   423|def generate_report(session_path: str, texts: List[str], features: Dict, 
   424|                    hub: Dict, cooccur: List, spiral: Dict) -> str:
   425|    """生成惯性坍缩报告"""
   426|    n = len(texts)
   427|    lines = []
   428|    lines.append("=" * 60)
   429|    lines.append("  惯性坍缩报告")
   430|    lines.append("=" * 60)
   431|    lines.append(f"  Session: {os.path.basename(session_path)}")
   432|    lines.append(f"  扫描轮数: {n}轮")
   433|    lines.append("")
   434|    
   435|    # 特征检测表
   436|    lines.append("  特征检测（10条）")
   437|    lines.append("  " + "-" * 56)
   438|    lines.append(f"  {'特征':<14} {'出现率':>6} {'均值':>6} {'最大':>6} {'Hub':<6}")
   439|    lines.append("  " + "-" * 56)
   440|    for fid in ["F01","F04","F06","F05","F07","F14","F08","F09","F19","F22"]:
   441|        d = features[fid]
   442|        bar = "█" * int(d["appear_rate"] * 10) + "░" * (10 - int(d["appear_rate"] * 10))
   443|        lines.append(f"  {fid} {d['name']:<8} {d['appear_rate']:>5.0%}  {d['mean']:.3f}  {d['max']:.3f}  {d['hub']:<6} {bar}")
   444|    lines.append("")
   445|    
   446|    # Hub活跃度
   447|    lines.append("  Hub活跃度")
   448|    for hub_name in ["Hub1", "Hub2", "Hub3", "Hub4"]:
   449|        v = hub[hub_name]
   450|        bar = "█" * int(v * 10) + "░" * (10 - int(v * 10))
   451|        label = {"Hub1": "输出自强化", "Hub2": "身份固化", "Hub3": "会话阶段", "Hub4": "合理化免疫"}[hub_name]
   452|        lines.append(f"  {hub_name} {label}: {bar} {v:.3f}")
   453|    lines.append("")
   454|    
   455|    # 惯性簇
   456|    if cooccur:
   457|        lines.append("  惯性簇（共现≥2次）")
   458|        for c in cooccur[:5]:
   459|            f1, f2 = c["features"]
   460|            lines.append(f"  {f1}({features[f1]['name']}) + {f2}({features[f2]['name']})  "
   461|                         f"共现{c['count']}次({c['rate']:.0%})  {c['hub']}")
   462|        lines.append("")
   463|    
   464|    # 时间线（前8轮或全部）
   465|    show_n = min(n, 12)
   466|    lines.append("  时间线（前{0}轮）".format(show_n))
   467|    header = "  轮次  " + "  ".join(f"{i+1:>4}" for i in range(show_n))
   468|    lines.append(header)
   469|    for fid in ["F01","F04","F06","F05","F08","F19"]:
   470|        scores = features[fid]["scores"][:show_n]
   471|        row = f"  {fid}    " + "  ".join(f"{s:.2f}" for s in scores)
   472|        lines.append(row)
   473|    lines.append("")
   474|    
   475|    # 螺旋方向
   476|    lines.append("  螺旋方向")
   477|    for fid in ["F01","F04","F06","F05","F14"]:
   478|        s = spiral[fid]
   479|        lines.append(f"  {fid} {features[fid]['name']:<8} {s['direction']}  Δ={s['delta']:+.4f}")
   480|    lines.append("")
   481|    
   482|    # 一句话锚点
   483|    # 找最显著的特征
   484|    top_fid = max(features.keys(), key=lambda f: features[f]["appear_rate"])
   485|    top_cluster = ""
   486|    if cooccur:
   487|        f1, f2 = cooccur[0]["features"]
   488|        top_cluster = f"{f1}+{f2}"
   489|    
   490|    # 整体螺旋判定
   491|    spiral_vals = [spiral[f]["delta"] for f in spiral if spiral[f]["direction"] != "insufficient_data"]
   492|    if spiral_vals:
   493|        avg_delta = sum(spiral_vals) / len(spiral_vals)
   494|        if avg_delta < -0.03:
   495|            spiral_verdict = "松动↑"
   496|        elif avg_delta > 0.03:
   497|            spiral_verdict = "强化↓"
   498|        else:
   499|            spiral_verdict = "持平→"
   500|    else:
   501|