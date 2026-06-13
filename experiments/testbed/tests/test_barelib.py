"""Ground-truth tests: barelib WORKS, it is just hostile to LLMs.
These must always pass — they prove failures in experiments come from
documentation/usability, not from bugs in the library."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from barelib import gmk, apx, flt, msk, agg, zst, ovl, rsz, thr, cnt, bbx, nbr, gsv, gld


def test_roundtrip(tmp_path):
    g = gmk(3, 2, 1.0)
    p = gsv(g, str(tmp_path / "g.csv"))
    assert gld(p) == g


def test_pipeline():
    g = gmk(4, 4, 2)
    g2 = apx(g, lambda x: x * 10)            # all 20
    m = thr(g2, 5)                            # all 1
    masked = msk(g2, m)
    assert agg(masked)["mean"] == 20
    zones = [[0, 0, 1, 1]] * 4
    z = zst(g2, zones)
    assert z[0]["n"] == 8 and z[1]["mean"] == 20
    o = ovl(g2, g2, lambda a, b: a + b)
    assert o[0][0] == 40
    assert cnt(thr(o, 30), 1) == 16
    assert rsz(g2, 2, 2)[0][0] == 20
    assert flt(g2, lambda x: x > 100, fill=-1)[0][0] == -1


def test_geometry():
    g = gmk(5, 5, 0)
    g[2][3] = 7
    assert bbx(g) == (2, 3, 2, 3)
    assert len(nbr(g, 0, 0)) == 3


def test_errors_are_terse():
    import pytest
    with pytest.raises(ValueError):
        gmk(0, 5)
    with pytest.raises(ValueError):
        agg([[None]])
