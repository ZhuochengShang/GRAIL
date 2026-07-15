import sys
import traceback

import MDAnalysis as mda
import numpy as np


def run():
    # AIDEAL_DATA_BINDINGS

    # TODO API_TEST_START
    # TODO API_TEST_END
    pass


if __name__ == "__main__":
    try:
        run()
        print("__DONE__")
    except Exception as exc:
        sys.stderr.write(f"__RUN_ERR__ {type(exc).__name__}: {exc}\n")
        traceback.print_exc()
        sys.exit(1)
