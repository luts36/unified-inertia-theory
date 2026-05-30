     1|#!/usr/bin/env python3
     2|"""
     3|inertia_monitor.py — 统一惯性理论 治理监测器
     4|============================================
     5|收束U1+U2+U4：阈值校准 + 渐变退化检测 + Agent治理接入
     6|
     7|功能：
     8|  1. calibrate  — 从历史session校准阈值（P1）
     9|  2. analyze    — 分析单个session（含渐变检测）（P2）
    10|  3. scan       — 扫描所有session，输出健康报告
    11|  4. live       — 实时监测模式（逐轮输入）
    12|  5. detail     — 详细分析（monitor指标 + 4条独有特征 + 共现分析 + 时间线）
    13|                   （原inertia-collapse降级合并，2026-05-28）
    14|  6. current    — 实时分析当前session（从.json文件读取，对话进行中即可用）
    15|                   解决"session文件对话结束后才写入"的阻塞问题（2026-05-29）
    16|
    17|依赖：inertia_metrics_v3.py（同目录）
    18|
    19|用法：
    20|  python3 inertia_monitor.py calibrate           # 校准阈值
    21|  python3 inertia_monitor.py scan                # 扫描所有session
    22|  python3 inertia_monitor.py analyze <session>   # 分析单个session
    23|  python3 inertia_monitor.py live                # 实时监测
    24|  python3 inertia_monitor.py detail <session>    # 详细分析（含独有特征）
    25|  python3 inertia_monitor.py current             # 实时分析当前session
    26|  python3 inertia_monitor.py report              # 完整报告（calibrate+scan）
    27|"""
    28|
    29|import sys, os, json, math
    30|from typing import Dict, List, Optional, Tuple
    31|
    32|# ══════════════════════════════════════════
    33|# 导入v3引擎
    34|# ══════════════════════════════════════════
    35|
    36|SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    37|sys.path.insert(0, SCRIPT_DIR)
    38|
    39|try:
    40|    from inertia_metrics_v3 import (
    41|        calc_I_new_v3, calc_H_session, calc_theta_v3,
    42|        calc_f_function, assess_v3, analyze_v3
    43|    )
    44|    HAS_V3 = True
    45|except ImportError:
    46|    HAS_V3 = False
    47|    print("ERROR: inertia_metrics_v3.py not found in", SCRIPT_DIR)
    48|    sys.exit(1)
    49|
    50|# ══════════════════════════════════════════
    51|# 会话读取
    52|# ══════════════════════════════════════════
    53|
    54|SESSION_DIR = os.environ.get("SESSION_DIR", os.path.expanduser("~/.sessions"))
    55|THRESHOLD_FILE = os.path.join(SCRIPT_DIR, "inertia_thresholds.json")
    56|
    57|
    58|def load_session_texts(session_path: str, max_chars: int = 800) -> List[str]:
    59|    """从JSONL session文件提取assistant消息文本"""
    60|    texts = []
    61|    try:
    62|        with open(session_path, 'r', encoding='utf-8') as f:
    63|            for line in f:
    64|                try:
    65|                    data = json.loads(line.strip())
    66|                except (json.JSONDecodeError, Exception):
    67|                    continue
    68|                role = data.get("role", "")
    69|                content = data.get("content", "")
    70|                if role == "assistant" and content and len(content) > 20:
    71|                    texts.append(content[:max_chars])
    72|    except Exception as e:
    73|        print(f"  Error reading {session_path}: {e}")
    74|    return texts
    75|
    76|
    77|def load_session_pairs(session_path: str, max_chars: int = 800) -> List[Dict]:
    78|    """从JSONL session文件提取user-assistant对"""
    79|    messages = []
    80|    try:
    81|        with open(session_path, 'r', encoding='utf-8') as f:
    82|            for line in f:
    83|                try:
    84|                    data = json.loads(line.strip())
    85|                except (json.JSONDecodeError, Exception):
    86|                    continue
    87|                role = data.get("role", "")
    88|                content = data.get("content", "")
    89|                if role in ("user", "assistant") and content and len(content) > 5:
    90|                    messages.append({"role": role, "content": content[:max_chars]})
    91|    except Exception:
    92|        pass
    93|    
    94|    pairs = []
    95|    for i in range(len(messages) - 1):
    96|        if messages[i]["role"] == "user" and messages[i+1]["role"] == "assistant":
    97|            pairs.append({
    98|                "context": messages[i]["content"],
    99|                "output": messages[i+1]["content"],
   100|            })
   101|    return pairs
   102|
   103|
   104|# ══════════════════════════════════════════
   105|# 实时session读取（.json格式，对话进行中即可读）
   106|# ══════════════════════════════════════════
   107|
   108|def load_session_json_texts(session_path: str, max_chars: int = 800) -> List[str]:
   109|    """从.json session文件（实时写入）提取assistant消息文本"""
   110|    try:
   111|        with open(session_path, 'r', encoding='utf-8') as f:
   112|            data = json.load(f)
   113|    except Exception as e:
   114|        print(f"  Error reading {session_path}: {e}")
   115|        return []
   116|    
   117|    messages = data.get("messages", [])
   118|    texts = []
   119|    for m in messages:
   120|        role = m.get("role", "")
   121|        content = m.get("content", "")
   122|        if role == "assistant" and content and len(content) > 20:
   123|            texts.append(content[:max_chars])
   124|    return texts
   125|
   126|
   127|def find_current_session() -> Optional[str]:
   128|    """找到当前活跃的session（最新修改的.json session文件）"""
   129|    if not os.path.isdir(SESSION_DIR):
   130|        return None
   131|    
   132|    json_sessions = []
   133|    for f in os.listdir(SESSION_DIR):
   134|        if f.startswith('session_') and f.endswith('.json') and 'cron' not in f and f != 'sessions.json':
   135|            full = os.path.join(SESSION_DIR, f)
   136|            json_sessions.append(full)
   137|    
   138|    if not json_sessions:
   139|        return None
   140|    
   141|    # 按修改时间排序，返回最新的
   142|    json_sessions.sort(key=lambda p: os.stat(p).st_mtime, reverse=True)
   143|    return json_sessions[0]
   144|
   145|
   146|def get_session_meta(session_path: str) -> Dict:
   147|    """获取.json session的元数据"""
   148|    try:
   149|        with open(session_path, 'r', encoding='utf-8') as f:
   150|            data = json.load(f)
   151|        return {
   152|            "session_id": data.get("session_id", "?"),
   153|            "model": data.get("model", "?"),
   154|            "platform": data.get("platform", "?"),
   155|            "session_start": data.get("session_start", "?"),
   156|            "last_updated": data.get("last_updated", "?"),
   157|            "message_count": data.get("message_count", 0),
   158|            "n_messages": len(data.get("messages", [])),
   159|        }
   160|    except Exception:
   161|        return {}
   162|
   163|
   164|def list_sessions() -> List[str]:
   165|    """列出所有session文件，按时间排序"""
   166|    if not os.path.isdir(SESSION_DIR):
   167|        return []
   168|    files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.jsonl')]
   169|    files.sort()
   170|    return [os.path.join(SESSION_DIR, f) for f in files]
   171|
   172|
   173|# ══════════════════════════════════════════
   174|# 渐变退化检测（线性回归趋势）
   175|# ══════════════════════════════════════════
   176|
   177|def detect_trend(values: List[float], min_points: int = 4) -> Dict:
   178|    """
   179|    线性回归检测渐变趋势
   180|    返回：slope, r_squared, direction, is_degrading
   181|    """
   182|    n = len(values)
   183|    if n < min_points:
   184|        return {"slope": 0, "r_squared": 0, "direction": "insufficient_data",
   185|                "is_degrading": False, "n": n}
   186|    
   187|    x_mean = (n - 1) / 2
   188|    y_mean = sum(values) / n
   189|    
   190|    # 线性回归
   191|    num = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
   192|    den = sum((i - x_mean) ** 2 for i in range(n))
   193|    slope = num / den if den > 0 else 0
   194|    
   195|    # R²
   196|    ss_res = sum((values[i] - (y_mean + slope * (i - x_mean))) ** 2 for i in range(n))
   197|    ss_tot = sum((v - y_mean) ** 2 for v in values)
   198|    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
   199|    
   200|    # 判断
   201|    if slope < -0.005 and r_squared > 0.3:
   202|        direction = "degrading"
   203|        is_degrading = True
   204|    elif slope > 0.005 and r_squared > 0.3:
   205|        direction = "improving"
   206|        is_degrading = False
   207|    else:
   208|        direction = "stable"
   209|        is_degrading = False
   210|    
   211|    return {
   212|        "slope": round(slope, 6),
   213|        "r_squared": round(r_squared, 4),
   214|        "direction": direction,
   215|        "is_degrading": is_degrading,
   216|        "n": n,
   217|    }
   218|
   219|
   220|# ══════════════════════════════════════════
   221|# 阈值校准
   222|# ══════════════════════════════════════════
   223|
   224|def calibrate_from_sessions(sessions: List[str]) -> Dict:
   225|    """
   226|    从历史session校准阈值
   227|    计算各指标的分布（mean, std, p95），用mean+2std作为告警阈值
   228|    """
   229|    all_L1 = []
   230|    all_delta_max = []
   231|    all_delta_std = []
   232|    all_H = []
   233|    all_theta = []
   234|    all_self_ref = []
   235|    
   236|    analyzed = 0
   237|    for sp in sessions:
   238|        texts = load_session_texts(sp)
   239|        if len(texts) < 3:
   240|            continue
   241|        
   242|        result = analyze_v3(texts)
   243|        I = result["I_new"]
   244|        H = result["H"]
   245|        theta = result["theta"]
   246|        f = result["f_function"]
   247|        
   248|        if I.get("status") == "ok":
   249|            all_L1.append(I["L1_mean"])
   250|            all_delta_max.append(I["delta_max"])
   251|            all_delta_std.append(I["delta_std"])
   252|        if H.get("status") == "ok":
   253|            all_H.append(H["H_mean"])
   254|        if theta.get("status") == "ok":
   255|            all_theta.append(theta["theta"])
   256|        all_self_ref.append(f.get("self_ref_density", 0))
   257|        analyzed += 1
   258|    
   259|    def stats(values, name):
   260|        if not values:
   261|            return {"mean": 0, "std": 0, "p95": 0, "n": 0, "threshold": 0}
   262|        n = len(values)
   263|        mean = sum(values) / n
   264|        std = (sum((v - mean)**2 for v in values) / n) ** 0.5
   265|        sorted_v = sorted(values)
   266|        p95_idx = min(int(n * 0.95), n - 1)
   267|        p95 = sorted_v[p95_idx]
   268|        threshold = min(mean + 2 * std, p95 * 1.2)  # 取更保守的
   269|        return {
   270|            "mean": round(mean, 4),
   271|            "std": round(std, 4),
   272|            "p95": round(p95, 4),
   273|            "n": n,
   274|            "threshold": round(threshold, 4),
   275|        }
   276|    
   277|    thresholds = {
   278|        "L1_mean": stats(all_L1, "L1_mean"),
   279|        "delta_max": stats(all_delta_max, "delta_max"),
   280|        "delta_std": stats(all_delta_std, "delta_std"),
   281|        "H_mean": stats(all_H, "H_mean"),
   282|        "theta": stats(all_theta, "theta"),
   283|        "self_ref_density": stats(all_self_ref, "self_ref_density"),
   284|        "sessions_analyzed": analyzed,
   285|        "calibration_time": __import__('datetime').datetime.now().isoformat(),
   286|    }
   287|    
   288|    return thresholds
   289|
   290|
   291|def save_thresholds(thresholds: Dict):
   292|    """保存阈值到文件"""
   293|    with open(THRESHOLD_FILE, 'w', encoding='utf-8') as f:
   294|        json.dump(thresholds, f, indent=2, ensure_ascii=False)
   295|    print(f"  阈值已保存: {THRESHOLD_FILE}")
   296|
   297|
   298|def load_thresholds() -> Optional[Dict]:
   299|    """加载已校准的阈值"""
   300|    if os.path.exists(THRESHOLD_FILE):
   301|        with open(THRESHOLD_FILE, 'r', encoding='utf-8') as f:
   302|            return json.load(f)
   303|    return None
   304|
   305|
   306|# ══════════════════════════════════════════
   307|# 健康评估（增强版：含渐变检测）
   308|# ══════════════════════════════════════════
   309|
   310|def assess_enhanced(I_new: Dict, H: Dict, theta: Dict, f_func: Dict,
   311|                    trend: Dict, thresholds: Optional[Dict] = None) -> Dict:
   312|    """
   313|    增强版健康评估：
   314|    - 继承v3的突变/自激检测
   315|    - 新增：渐变退化检测（趋势分析）
   316|    - 新增：阈值校准后的相对判定
   317|    """
   318|    alerts = []
   319|    actions = []
   320|    
   321|    l1 = I_new.get("L1_mean", 0.5)
   322|    h_mean = H.get("H_mean", 0.5)
   323|    delta_max = I_new.get("delta_max", 0)
   324|    delta_std = I_new.get("delta_std", 0)
   325|    theta_val = theta.get("theta", 0)
   326|    self_ref = f_func.get("self_ref_density", 0)
   327|    
   328|    # === 阈值：校准优先，硬编码兜底 ===
   329|    th_delta_max = thresholds.get("delta_max", {}).get("threshold", 0.55) if thresholds else 0.55
   330|    th_delta_std = thresholds.get("delta_std", {}).get("threshold", 0.16) if thresholds else 0.16
   331|    th_theta = thresholds.get("theta", {}).get("threshold", 0.75) if thresholds else 0.75
   332|    th_self_ref = thresholds.get("self_ref_density", {}).get("threshold", 0.5) if thresholds else 0.5
   333|    
   334|    # === 检测 ===
   335|    
   336|    # 自激循环（硬编码：L1高+H极高=循环，不依赖校准）
   337|    if l1 > 0.7 and h_mean > 0.85:
   338|        alerts.append(f"自激循环: L1={l1:.2f}+重叠={h_mean:.2f}")
   339|        actions.append("紧急: 注入外部信息打断循环")
   340|    
   341|    # 突变
   342|    if delta_max > th_delta_max:
   343|        alerts.append(f"突变: maxΔ={delta_max:.2f} > {th_delta_max:.2f}")
   344|        actions.append("检查: Agent是否偏离轨道")
   345|    
   346|    # 漂移
   347|    if delta_std > th_delta_std:
   348|        alerts.append(f"漂移: δ_std={delta_std:.2f} > {th_delta_std:.2f}")
   349|        actions.append("检查: 行为是否不稳定")
   350|    
   351|    # 偏离
   352|    if theta_val > th_theta:
   353|        alerts.append(f"偏离: θ={theta_val:.2f} > {th_theta:.2f}")
   354|        actions.append("检查: 是否需重新引导")
   355|    
   356|    # 自激
   357|    if self_ref > th_self_ref:
   358|        alerts.append(f"自激: 自引用={self_ref:.2f} > {th_self_ref:.2f}")
   359|        actions.append("考虑: 注入外部信息")
   360|    
   361|    # === 新增：渐变退化 ===
   362|    
   363|    if trend.get("is_degrading"):
   364|        slope = trend["slope"]
   365|        r2 = trend["r_squared"]
   366|        alerts.append(f"渐变退化: slope={slope:.4f} R²={r2:.2f}")
   367|        actions.append("关注: 行为延续度在持续下降，可能需要干预")
   368|    
   369|    # === 新增：阈值校准后的相对判定 ===
   370|    
   371|    if thresholds:
   372|        th = thresholds
   373|        if l1 > th.get("L1_mean", {}).get("threshold", 999):
   374|            alerts.append(f"超阈值: L1={l1:.2f} > {th['L1_mean']['threshold']:.2f}")
   375|        if delta_max > th.get("delta_max", {}).get("threshold", 999):
   376|            alerts.append(f"超阈值: Δmax={delta_max:.2f} > {th['delta_max']['threshold']:.2f}")
   377|    
   378|    # === 健康判定 ===
   379|    
   380|    has_critical = any("自激循环" in a for a in alerts)
   381|    has_warning = any("突变" in a or "偏离" in a or "渐变退化" in a for a in alerts)
   382|    has_info = len(alerts) > 0
   383|    
   384|    if has_critical:
   385|        health = "危险"
   386|    elif has_warning:
   387|        health = "警告"
   388|    elif has_info:
   389|        health = "注意"
   390|    else:
   391|        health = "健康"
   392|    
   393|    return {
   394|        "health": health,
   395|        "alerts": alerts,
   396|        "actions": actions,
   397|        "trend": trend,
   398|        "summary": alerts[0] if alerts else "所有指标正常",
   399|    }
   400|
   401|
   402|# ══════════════════════════════════════════
   403|# 分析单个session
   404|# ══════════════════════════════════════════
   405|
   406|def analyze_session(session_path: str, thresholds: Optional[Dict] = None) -> Dict:
   407|    """完整分析单个session"""
   408|    texts = load_session_texts(session_path)
   409|    if len(texts) < 3:
   410|        return {"status": "insufficient_data", "n_texts": len(texts)}
   411|    
   412|    # v3指标
   413|    I_new = calc_I_new_v3(texts)
   414|    H = calc_H_session(texts)
   415|    theta = calc_theta_v3(texts)
   416|    f_func = calc_f_function(sum(len(t) for t in texts), texts)
   417|    
   418|    # 渐变检测：对I序列做趋势分析
   419|    # 需要逐对计算I值序列
   420|    model = None
   421|    try:
   422|        from inertia_metrics_v3 import get_embedding_model
   423|        model = get_embedding_model()
   424|    except:
   425|        pass
   426|    
   427|    I_sequence = []
   428|    if model is not None:
   429|        import math as m
   430|        embs = model.encode(texts, show_progress_bar=False)
   431|        for i in range(1, len(embs)):
   432|            dot = sum(a*b for a, b in zip(embs[i-1].tolist(), embs[i].tolist()))
   433|            n1 = m.sqrt(sum(a**2 for a in embs[i-1].tolist()))
   434|            n2 = m.sqrt(sum(b**2 for b in embs[i].tolist()))
   435|            sim = dot / (n1 * n2) if n1 > 0 and n2 > 0 else 0
   436|            I_sequence.append(sim)
   437|    else:
   438|        # fallback: 关键词重叠
   439|        import re
   440|        for i in range(1, len(texts)):
   441|            kw_prev = set(re.findall(r'[\u4e00-\u9fff]{2,}', texts[i-1]))
   442|            kw_curr = set(re.findall(r'[\u4e00-\u9fff]{2,}', texts[i]))
   443|            if kw_prev and kw_curr:
   444|                I_sequence.append(len(kw_prev & kw_curr) / len(kw_prev | kw_curr))
   445|            else:
   446|                I_sequence.append(0)
   447|    
   448|    trend = detect_trend(I_sequence)
   449|    
   450|    # 增强评估
   451|    health = assess_enhanced(I_new, H, theta, f_func, trend, thresholds)
   452|    
   453|    return {
   454|        "session": os.path.basename(session_path),
   455|        "n_texts": len(texts),
   456|        "I_new": I_new,
   457|        "H": H,
   458|        "theta": theta,
   459|        "f_function": f_func,
   460|        "trend": trend,
   461|        "health": health,
   462|    }
   463|
   464|
   465|# ══════════════════════════════════════════
   466|# 扫描所有session
   467|# ══════════════════════════════════════════
   468|
   469|def scan_all(thresholds: Optional[Dict] = None) -> List[Dict]:
   470|    """扫描所有session，返回健康报告"""
   471|    sessions = list_sessions()
   472|    results = []
   473|    for sp in sessions:
   474|        r = analyze_session(sp, thresholds)
   475|        if r.get("status") != "insufficient_data":
   476|            results.append(r)
   477|    return results
   478|
   479|
   480|# ══════════════════════════════════════════
   481|# 报告输出
   482|# ══════════════════════════════════════════
   483|
   484|def print_threshold_report(thresholds: Dict):
   485|    """打印阈值校准报告"""
   486|    print("=" * 60)
   487|    print("  阈值校准报告")
   488|    print("=" * 60)
   489|    print(f"  分析session数: {thresholds.get('sessions_analyzed', 0)}")
   490|    print(f"  校准时间: {thresholds.get('calibration_time', 'N/A')}")
   491|    print()
   492|    
   493|    for metric in ["L1_mean", "delta_max", "delta_std", "H_mean", "theta", "self_ref_density"]:
   494|        s = thresholds.get(metric, {})
   495|        if s.get("n", 0) > 0:
   496|            print(f"  {metric:20s}  mean={s['mean']:.4f}  std={s['std']:.4f}  "
   497|                  f"p95={s['p95']:.4f}  → 阈值={s['threshold']:.4f}")
   498|    print()
   499|
   500|
   501|