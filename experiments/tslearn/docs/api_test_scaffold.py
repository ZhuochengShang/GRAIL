# AIDEAL API-test scaffold (Python) — the generated snippet is spliced between
# the API_TEST markers and runs inside run(). Success = "__DONE__" on stdout
# and exit 0; any exception prints "__RUN_ERR__ <Type>: <msg>" plus traceback.
import sys
import traceback

import numpy as np
from tslearn.generators import random_walks  # preamble dataset source


def run():
    # Typed sample inputs (comprehension.execute.sample_data):
    # AIDEAL_DATA_BINDINGS

    # Isolate audience imports/assignments from the fixture preamble. In
    # particular, `import numpy as np` inside this nested scope must not make
    # `np` local to run() before the preamble has loaded Trace.npz.
    def api_test():
        # TODO API_TEST_START
        # TODO API_TEST_END
        pass

    api_test()
    pass


if __name__ == "__main__":
    try:
        run()
        print("__DONE__")
    except Exception as e:  # noqa: BLE001 — harness boundary
        sys.stderr.write("__RUN_ERR__ " + type(e).__name__ + ": " + str(e) + "\n")
        traceback.print_exc()
        sys.exit(1)
