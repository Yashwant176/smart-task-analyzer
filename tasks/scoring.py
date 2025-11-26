from datetime import datetime, date
from collections import defaultdict, deque

class CircularDependencyError(Exception):
    pass

def _build_maps(tasks):
    """Create id map and adjacency list for given tasks list of dicts."""
    id_map = {}
    for i, t in enumerate(tasks):
        tid = t.get('id')
        if tid is None:
            tid = i + 1
            t['id'] = tid
        id_map[tid] = t

    adj = defaultdict(list)
    for t in tasks:
        tid = t['id']
        for dep in t.get('dependencies', []):
            if dep in id_map:
                adj[tid].append(dep)
    return id_map, adj

def detect_cycle(adj):
    """Return True if directed graph has cycle via Kahn's algorithm."""
    indegree = {}
    nodes = set()
    for u, vs in adj.items():
        nodes.add(u)
        for v in vs:
            nodes.add(v)
    for n in nodes:
        indegree[n] = 0
    for u, vs in adj.items():
        for v in vs:
            indegree[v] = indegree.get(v, 0) + 1
    queue = deque([n for n in nodes if indegree.get(n, 0) == 0])
    visited = 0
    while queue:
        u = queue.popleft()
        visited += 1
        for v in adj.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return visited != len(nodes)

def _days_until_due(due_date):
    if due_date is None:
        return None
    today = date.today()
    return (due_date - today).days

def _normalize(val, vmin, vmax):
    if vmax == vmin:
        return 1.0
    return (val - vmin) / (vmax - vmin)

def analyze_tasks(task_list, strategy='smart_balance'):
    """
    Accepts list of task dicts and returns list of tasks with 'score' and 'explanation'.
    strategy options: smart_balance, fastest_wins, high_impact, deadline_driven
    """
    tasks = [dict(t) for t in task_list]  # defensive copy

    id_map, adj = _build_maps(tasks)

    # Build dependents count (how many tasks depend on this task)
    dependents_count = defaultdict(int)
    for t in tasks:
        for dep in t.get('dependencies', []):
            dependents_count[dep] += 1

    # Detect circular dependencies
    if detect_cycle(adj):
        raise CircularDependencyError("Circular dependencies detected among tasks.")

    # Precompute raw metrics
    urgencies = []
    importances = []
    efforts = []
    deps = []
    for t in tasks:
        dd = t.get('due_date', None)
        if isinstance(dd, str):
            try:
                dd = datetime.strptime(dd, "%Y-%m-%d").date()
            except Exception:
                dd = None
        t['__due_date_obj'] = dd
        days = _days_until_due(dd)
        days_for_norm = 3650 if days is None else days
        urgencies.append(days_for_norm)

        importance = float(t.get('importance', 5))
        importances.append(importance)

        effort = float(t.get('estimated_hours', 1.0))
        efforts.append(effort)

        dep_score = float(dependents_count.get(t['id'], 0))
        deps.append(dep_score)

    # Normalize
    min_days, max_days = min(urgencies), max(urgencies)
    norm_urgencies = []
    for d in urgencies:
        n = _normalize(d, min_days, max_days)
        n = 1.0 - n
        if d < 0:
            boost = min(1.0, (abs(d) / 30.0))
            n = min(1.0, n + 0.5 * boost)
        norm_urgencies.append(n)

    min_imp, max_imp = min(importances), max(importances)
    norm_importances = [_normalize(v, min_imp, max_imp) for v in importances]

    min_eff, max_eff = min(efforts), max(efforts)
    norm_efforts = []
    for e in efforts:
        n = _normalize(e, min_eff, max_eff)
        n = 1.0 - n
        if e <= 1:
            n = min(1.0, n + 0.1)
        norm_efforts.append(n)

    min_dep, max_dep = min(deps), max(deps)
    if min_dep == max_dep:
        norm_deps = [1.0 if v > 0 else 0.0 for v in deps]
    else:
        norm_deps = [_normalize(v, min_dep, max_dep) for v in deps]

    strategies = {
        'smart_balance': {'urgency':0.35, 'importance':0.35, 'effort':0.15, 'dependencies':0.15},
        'fastest_wins':  {'urgency':0.15, 'importance':0.2,  'effort':0.5,  'dependencies':0.15},
        'high_impact':   {'urgency':0.15, 'importance':0.6,  'effort':0.1,  'dependencies':0.15},
        'deadline_driven':{'urgency':0.6, 'importance':0.2,  'effort':0.05, 'dependencies':0.15},
    }
    weights = strategies.get(strategy, strategies['smart_balance'])

    scored = []
    for idx, t in enumerate(tasks):
        u = norm_urgencies[idx]
        im = norm_importances[idx]
        ef = norm_efforts[idx]
        de = norm_deps[idx]

        score_raw = (weights['urgency'] * u +
                     weights['importance'] * im +
                     weights['effort'] * ef +
                     weights['dependencies'] * de)
        score = round(score_raw * 100, 2)

        reasons = [
            f"Urgency: {round(u,2)}",
            f"Importance: {round(im,2)}",
            f"Effort (quick-win): {round(ef,2)}",
            f"Blocks other tasks: {round(de,2)}"
        ]
        explanation = "; ".join(reasons)

        out = dict(t)
        out['score'] = score
        out['explanation'] = explanation
        scored.append(out)

    scored_sorted = sorted(scored, key=lambda x: x['score'], reverse=True)
    return scored_sorted
