     1|#!/usr/bin/env python3
     2|"""
     3|inertia_auto_check.py — 惯性医生自动体检 v2.0
     4|================================================
     5|运行 monitor.current → 解析指标 → 分级触发判断 → 冷却期管理
     6|
     7|用法：
     8|  python3 inertia_auto_check.py          # 自动体检，异常时输出建议
     9|  python3 inertia_auto_check.py --force  # 强制输出（不管健康与否）
    10|  python3 inertia_auto_check.py --json   # JSON格式输出（供Agent解析）
    11|  python3 inertia_auto_check.py --disable # 关闭自动触发
    12|
    13|分级触发策略（A/B实验数据驱动）：
    14|  阶段错配 → 前3轮必检（效果最好，满分5.0）
    15|  F01锚定 → 每5轮检
    16|  H自激 → H>0.7时触发
    17|  模式锁定 → 输出模板复用时检
    18|  身份固化 → 任务类型切换时检
    19|  θ偏离 → 每次任务切换检（最难治，需最灵敏）
    20|
    21|冷却期：同一类型触发后，至少间隔3轮再触发
    22|"""
    23|
    24|import sys, os, json, re, subprocess, math
    25|
    26|SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    27|MONITOR = os.path.join(SCRIPT_DIR, "inertia_monitor.py")
    28|
    29|# ══════════════════════════════════════════
    30|# 运行 monitor current
    31|# ══════════════════════════════════════════
    32|
    33|def run_monitor_current():
    34|    """运行 monitor.py current，返回stdout"""
    35|    try:
    36|        result = subprocess.run(
    37|            ["python3", MONITOR, "current"],
    38|            capture_output=True, text=True, timeout=120
    39|        )
    40|        return result.stdout, result.returncode
    41|    except subprocess.TimeoutExpired:
    42|        return "ERROR: monitor timeout", 2
    43|    except Exception as e:
    44|        return f"ERROR: {e}", 2
    45|
    46|
    47|# ══════════════════════════════════════════
    48|# 解析 monitor 输出
    49|# ══════════════════════════════════════════
    50|
    51|def parse_monitor_output(stdout):
    52|    """从monitor输出中提取指标"""
    53|    data = {}
    54|    
    55|    # 提取 session_id
    56|    m = re.search(r'Session:\s+(\S+)', stdout)
    57|    if m:
    58|        data['session_id'] = m.group(1)
    59|    
    60|    # 提取 assistant 消息数
    61|    m = re.search(r'assistant:\s*(\d+)', stdout)
    62|    if m:
    63|        data['n_assistant'] = int(m.group(1))
    64|    
    65|    # 提取指标行: L1=0.559  Δmax=0.234  H=0.679  θ=0.493  trend=improving  health=健康
    66|    m = re.search(r'L1=([\d.]+)\s+Δmax=([\d.]+)\s+H=([\d.]+)\s+θ=([\d.]+)\s+trend=(\S+)\s+health=(\S+)', stdout)
    67|    if m:
    68|        data['L1'] = float(m.group(1))
    69|        data['delta_max'] = float(m.group(2))
    70|        data['H'] = float(m.group(3))
    71|        data['theta'] = float(m.group(4))
    72|        data['trend'] = m.group(5)
    73|        data['health'] = m.group(6)
    74|    
    75|    # 提取 if-then 规则触发
    76|    if '自激循环' in stdout:
    77|        data['rule'] = '自激循环'
    78|        data['severity'] = 'critical'
    79|    elif '自激预警' in stdout:
    80|        data['rule'] = '自激预警'
    81|        data['severity'] = 'warning'
    82|    elif '偏离' in stdout and 'θ=' in stdout:
    83|        data['rule'] = '偏离'
    84|        data['severity'] = 'warning'
    85|    elif '锚定过强' in stdout:
    86|        data['rule'] = '锚定过强'
    87|        data['severity'] = 'warning'
    88|    elif '注意力混乱' in stdout:
    89|        data['rule'] = '注意力混乱'
    90|        data['severity'] = 'warning'
    91|    elif '好惯性' in stdout:
    92|        data['rule'] = '好惯性'
    93|        data['severity'] = 'ok'
    94|    elif '中性' in stdout:
    95|        data['rule'] = '中性'
    96|        data['severity'] = 'neutral'
    97|    else:
    98|        data['rule'] = 'unknown'
    99|        data['severity'] = 'unknown'
   100|    
   101|    # 提取特征数据
   102|    features = {}
   103|    for fid in ['F05', 'F07', 'F14', 'F09']:
   104|        m = re.search(rf'{fid}\s+\S+\s+([\d.]+)%\s+([\d.]+)', stdout)
   105|        if m:
   106|            features[fid] = {'rate': float(m.group(1)), 'mean': float(m.group(2))}
   107|    data['features'] = features
   108|    
   109|    return data
   110|
   111|
   112|# ══════════════════════════════════════════
   113|# 分级触发策略（A/B实验数据驱动）
   114|# ══════════════════════════════════════════
   115|
   116|# 冷却期记录文件
   117|COOLDOWN_FILE = os.environ.get("COOLDOWN_FILE", os.path.expanduser("~/.cache/inertia_auto_check_cooldown.json"))
   118|
   119|def load_cooldown():
   120|    """加载冷却期记录"""
   121|    try:
   122|        if os.path.exists(COOLDOWN_FILE):
   123|            with open(COOLDOWN_FILE, 'r') as f:
   124|                return json.load(f)
   125|    except:
   126|        pass
   127|    return {}
   128|
   129|def save_cooldown(cooldown):
   130|    """保存冷却期记录"""
   131|    os.makedirs(os.path.dirname(COOLDOWN_FILE), exist_ok=True)
   132|    with open(COOLDOWN_FILE, 'w') as f:
   133|        json.dump(cooldown, f)
   134|
   135|def check_cooldown(rule, cooldown_rounds=3):
   136|    """检查是否在冷却期内"""
   137|    cooldown = load_cooldown()
   138|    if rule in cooldown:
   139|        last_trigger = cooldown[rule]
   140|        return last_trigger < cooldown_rounds
   141|    return False
   142|
   143|def update_cooldown(rule):
   144|    """更新冷却期记录"""
   145|    cooldown = load_cooldown()
   146|    cooldown[rule] = 0
   147|    for k in list(cooldown.keys()):
   148|        if k != rule:
   149|            cooldown[k] = cooldown.get(k, 0) + 1
   150|    save_cooldown(cooldown)
   151|
   152|def get_trigger_strategy(data):
   153|    """基于A/B实验数据的分级触发策略"""
   154|    rule = data.get('rule', 'unknown')
   155|    severity = data.get('severity', 'unknown')
   156|    n_assistant = data.get('n_assistant', 0)
   157|    H = data.get('H', 0.5)
   158|    theta = data.get('theta', 0)
   159|    
   160|    # 基础判断：健康状态不触发
   161|    if severity in ('ok', 'neutral'):
   162|        return False, 'healthy'
   163|    
   164|    # 分级触发策略
   165|    strategies = {
   166|        '阶段错配': {'early_rounds': 3, 'description': '前3轮必检'},
   167|        '锚定过强': {'interval': 5, 'description': '每5轮检'},
   168|        '自激循环': {'threshold': 'H>0.85', 'description': '症状明确才介入'},
   169|        '自激预警': {'threshold': 'H<0.3', 'description': '症状明确才介入'},
   170|        '偏离': {'interval': 3, 'description': '每次任务切换检'},
   171|        '注意力混乱': {'interval': 5, 'description': '每5轮检'},
   172|    }
   173|    
   174|    strategy = strategies.get(rule, {'interval': 5, 'description': '默认每5轮'})
   175|    
   176|    # 阶段错配：前3轮必检
   177|    if rule == '阶段错配' and n_assistant <= 3:
   178|        return True, f'阶段错配早期检测(第{n_assistant}轮)'
   179|    
   180|    # 自激类：基于H阈值
   181|    if rule in ('自激循环', '自激预警'):
   182|        if rule == '自激循环' and H > 0.85:
   183|            return True, f'自激循环(H={H:.2f}>0.85)'
   184|        elif rule == '自激预警' and H < 0.3:
   185|            return True, f'自激预警(H={H:.2f}<0.3)'
   186|        return False, f'{rule}阈值未达'
   187|    
   188|    # 其他类型：基于间隔
   189|    interval = strategy.get('interval', 5)
   190|    if n_assistant % interval == 0:
   191|        return True, f'{rule}(每{interval}轮)'
   192|    
   193|    return False, f'{rule}未到触发间隔'
   194|
   195|def needs_intervention(data):
   196|    """判断是否需要医生介入（分级触发版本）"""
   197|    severity = data.get('severity', 'unknown')
   198|    
   199|    if severity not in ('critical', 'warning'):
   200|        return False
   201|    
   202|    rule = data.get('rule', 'unknown')
   203|    if check_cooldown(rule):
   204|        return False
   205|    
   206|    should_trigger, reason = get_trigger_strategy(data)
   207|    
   208|    if should_trigger:
   209|        update_cooldown(rule)
   210|        return True
   211|    
   212|    return False
   213|
   214|
   215|# ══════════════════════════════════════════
   216|# 主程序
   217|# ══════════════════════════════════════════
   218|
   219|def main():
   220|    force = '--force' in sys.argv
   221|    json_out = '--json' in sys.argv
   222|    disable = '--disable' in sys.argv
   223|    
   224|    # --disable 开关
   225|    if disable:
   226|        if json_out:
   227|            print(json.dumps({"status": "disabled", "message": "自动触发已关闭"}, ensure_ascii=False))
   228|        else:
   229|            print("⏸ 惯性医生自动触发已关闭")
   230|        sys.exit(0)
   231|    
   232|    stdout, rc = run_monitor_current()
   233|    
   234|    # 数据不足
   235|    if '数据不足' in stdout or rc == 2:
   236|        if json_out:
   237|            print(json.dumps({"status": "insufficient_data", "raw": stdout[:200]}, ensure_ascii=False))
   238|        else:
   239|            print("⏸ 数据不足，跳过体检")
   240|        sys.exit(2)
   241|    
   242|    # 解析
   243|    data = parse_monitor_output(stdout)
   244|    
   245|    if json_out:
   246|        print(json.dumps(data, ensure_ascii=False, indent=2))
   247|        sys.exit(0 if not needs_intervention(data) else 1)
   248|    
   249|    # 人类可读输出
   250|    severity = data.get('severity', 'unknown')
   251|    rule = data.get('rule', 'unknown')
   252|    health = data.get('health', '?')
   253|    
   254|    if not force and not needs_intervention(data):
   255|        sys.exit(0)
   256|    
   257|    icon = {'critical': '🔴', 'warning': '⚡', 'ok': '✅', 'neutral': '👀'}.get(severity, '❓')
   258|    
   259|    print()
   260|    print(f"  {icon} 惯性体检告警")
   261|    print(f"  {'='*50}")
   262|    print(f"  Session: {data.get('session_id', '?')}")
   263|    print(f"  Messages: {data.get('n_assistant', '?')} assistant")
   264|    print(f"  L1={data.get('L1', 0):.3f}  H={data.get('H', 0):.3f}  θ={data.get('theta', 0):.3f}")
   265|    print(f"  Trend: {data.get('trend', '?')}")
   266|    print(f"  Health: {health}")
   267|    print(f"  Rule: {rule}")
   268|    print(f"  {'='*50}")
   269|    print()
   270|    print(f"  医生需要介入。运行惯性分析获取建议。")
   271|    print()
   272|    
   273|    sys.exit(1)
   274|
   275|
   276|if __name__ == "__main__":
   277|    main()
   278|