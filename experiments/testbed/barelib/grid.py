# barelib: deliberately LLM-hostile baseline library.
# Cryptic names, no docstrings, terse unhelpful errors — BY DESIGN.
# Do not "improve" this file directly; improvements happen through the
# AIDEAL pipeline (LLM_readme, aliases module, error mapping) so each
# step's effect can be measured. A grid is a list of equal-length lists.


def gmk(w, h, v=0):
    if w <= 0 or h <= 0:
        raise ValueError("bad")
    return [[v for _ in range(w)] for _ in range(h)]


def gld(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append([float(x) for x in line.split(",")])
    if not rows or len({len(r) for r in rows}) != 1:
        raise ValueError("bad")
    return rows


def gsv(g, path):
    with open(path, "w") as f:
        for r in g:
            f.write(",".join(str(x) for x in r) + "\n")
    return path


def apx(g, f):
    return [[f(x) for x in r] for r in g]


def flt(g, p, fill=None):
    return [[x if p(x) else fill for x in r] for r in g]


def msk(g, m):
    if len(m) != len(g) or len(m[0]) != len(g[0]):
        raise ValueError("bad")
    return [[x if m[i][j] else None for j, x in enumerate(r)] for i, r in enumerate(g)]


def agg(g):
    vals = [x for r in g for x in r if x is not None]
    if not vals:
        raise ValueError("bad")
    return {"n": len(vals), "sum": sum(vals), "min": min(vals),
            "max": max(vals), "mean": sum(vals) / len(vals)}


def zst(g, zones):
    if len(zones) != len(g) or len(zones[0]) != len(g[0]):
        raise ValueError("bad")
    out = {}
    for i, r in enumerate(g):
        for j, x in enumerate(r):
            if x is None:
                continue
            out.setdefault(zones[i][j], []).append(x)
    return {z: {"n": len(v), "mean": sum(v) / len(v)} for z, v in out.items()}


def ovl(a, b, f):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("bad")
    return [[f(x, b[i][j]) if x is not None and b[i][j] is not None else None
             for j, x in enumerate(r)] for i, r in enumerate(a)]


def rsz(g, w, h):
    if w <= 0 or h <= 0:
        raise ValueError("bad")
    sh, sw = len(g), len(g[0])
    return [[g[int(i * sh / h)][int(j * sw / w)] for j in range(w)] for i in range(h)]


def thr(g, t):
    return [[None if x is None else (1 if x >= t else 0) for x in r] for r in g]


def cnt(g, v):
    return sum(1 for r in g for x in r if x == v)


def bbx(g):
    pts = [(i, j) for i, r in enumerate(g) for j, x in enumerate(r) if x]
    if not pts:
        raise ValueError("bad")
    return (min(p[0] for p in pts), min(p[1] for p in pts),
            max(p[0] for p in pts), max(p[1] for p in pts))


def nbr(g, x, y):
    if not (0 <= y < len(g) and 0 <= x < len(g[0])):
        raise IndexError("bad")
    out = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if (dx or dy) and 0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]):
                out.append(g[y + dy][x + dx])
    return out
