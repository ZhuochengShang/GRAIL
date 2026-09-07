import numpy as np

from mir_eval import beat, chord, io, melody, segment


def main():
    ref_events = np.array([0.0, 0.5, 1.0, 1.5])
    est_events = np.array([0.02, 0.48, 1.03, 1.52])
    assert 0.9 <= beat.f_measure(ref_events, est_events) <= 1.0

    intervals = np.array([[0.0, 0.5], [0.5, 1.0]])
    labels = ["C:maj", "G:maj"]
    assert chord.validate(labels, labels) is None
    assert segment.validate_boundary(intervals, intervals, trim=False) is None

    ref_voiced, ref_cents, est_voiced, est_cents = melody.to_cent_voicing(
        np.array([0.0, 0.5]), np.array([440.0, 0.0]),
        np.array([0.0, 0.5]), np.array([442.0, 0.0]))
    assert all(len(x) == 2 for x in
               (ref_voiced, ref_cents, est_voiced, est_cents))

    loaded = io.load_events("tests/data/beat/ref00.txt")
    assert loaded.ndim == 1 and loaded.size > 0
    print("__DONE__ mir_eval smoke", loaded.size)


if __name__ == "__main__":
    main()
