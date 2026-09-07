# pymatgen — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `AdditionalConditionInt`

### Signature
```python
class AdditionalConditionInt(int, StrategyOption)
```
_Source: source/src/pymatgen/analysis/chemenv/coordination_environments/chemenv_strategies.py:160_

_Source doc:_ Integer representing an additional condition in a strategy.

### Goal
Represents an integer-based additional condition option used within chemical environment coordination strategies.

### Parameters
_None._

### Input
A valid integer representing a specific condition for a coordination environment strategy. The integer must be within the allowed condition range (e.g., `3`). Floats and unsupported integers (e.g., `5`) are strictly prohibited and will fail validation upon instantiation.

### Output
Returns `unspecified` — An instance of `AdditionalConditionInt` that functions as both a standard Python integer and a `StrategyOption`. It supports serialization and deserialization via `.as_dict()` and `.from_dict()`.

### Valid Call Patterns
```python
# Instantiate with a valid integer condition
acd1 = AdditionalConditionInt(3)

# Serialize to a dictionary
acd1_dict = acd1.as_dict()

# Deserialize from a dictionary
acd2 = AdditionalConditionInt.from_dict(acd1_dict)
```

### LLM Instruction Prompt
- When instantiating `AdditionalConditionInt`, you MUST provide a valid integer (e.g., `3`). 
- Do NOT pass floats or unsupported integers (like `5`), as the class enforces strict value checking and will raise a `ValueError`.

### Prompt Snippet
```text
To configure the chemical environment strategy, instantiate the condition using a valid integer:
condition = AdditionalConditionInt(3)
```

### Common Failure Modes
- **Passing an unsupported integer:** Instantiating with an unallowed condition number (e.g., `AdditionalConditionInt(5)`) raises a `ValueError` matching `"Additional condition 5 is not allowed"`.
- **Passing a float:** Instantiating with a floating-point number (e.g., `AdditionalConditionInt(0.458)`) raises a `ValueError` matching `"Additional condition 0.458 is not an integer"`.

### Fix Code Hint
```python
# BAD: Passing a float or an unallowed integer
# condition = AdditionalConditionInt(5)
# condition = AdditionalConditionInt(0.458)

# GOOD: Passing a valid integer
condition = AdditionalConditionInt(3)
```

## API Test: `AflowPrototypeMatcher`

### Signature
```python
class AflowPrototypeMatcher(PrototypeDatabaseMatcher)
```
_Source: source/src/pymatgen/analysis/prototypes/matcher.py:138_

_Source doc:_ Deprecated alias for :class:`PrototypeDatabaseMatcher`. This class uses data from the AFLOW LIBRARY OF CRYSTALLOGRAPHIC PROTOTYPES. If using this class please cite their publication appropriately: Mehl, M. J., Hicks, D., Toher, C., Levy, O., Hanson, R. M., Hart, G., & Curtarolo, S. (2017). The AFLOW library of crystallographic prototypes: part 1. Computational Materials Science, 136, S1-S828. https://doi.org/10.1016/j.commatsci.2017.01.017

### Goal
`AflowPrototypeMatcher` is a deprecated alias for `PrototypeDatabaseMatcher` used to match crystal structures against the AFLOW Library of Crystallographic Prototypes.

### Parameters
_None._

### Input
No parameters are required for initialization. 

### Output
Returns `unspecified` — an instance of `AflowPrototypeMatcher` (which inherits from `PrototypeDatabaseMatcher`) that can be used to evaluate structural prototype matches.

### Valid Call Patterns
```python
import pytest

# Instantiation raises a DeprecationWarning
with pytest.warns(DeprecationWarning, match="AflowPrototypeMatcher is deprecated"):
    af = AflowPrototypeMatcher()
```

### LLM Instruction Prompt
- Do not use `AflowPrototypeMatcher` for new code; it is a deprecated alias. Use `PrototypeDatabaseMatcher` instead.
- If you must use `AflowPrototypeMatcher` to satisfy a specific legacy requirement or test fixture, you must account for the `DeprecationWarning` it raises upon instantiation.
- If using this class in a scientific workflow, ensure the AFLOW publication (Mehl et al., 2017) is cited appropriately.

### Prompt Snippet
```text
`AflowPrototypeMatcher` is a deprecated alias for `PrototypeDatabaseMatcher` in pymatgen. It takes no initialization parameters and raises a `DeprecationWarning` when instantiated. Prefer `PrototypeDatabaseMatcher` for modern workflows.
```

### Common Failure Modes
- **Strict Warning Failures:** Instantiating `AflowPrototypeMatcher` in a test suite or environment that treats warnings as errors will cause a crash due to the `DeprecationWarning`.

### Fix Code Hint
```python
# Instead of using the deprecated alias:
# af = AflowPrototypeMatcher()

# Use the modern class (assuming it is imported):
af = PrototypeDatabaseMatcher()

# Or, if legacy compatibility is strictly required, suppress/catch the warning:
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    af = AflowPrototypeMatcher()
```

## API Test: `AllCoordinationGeometries`

### Signature
```python
class AllCoordinationGeometries(dict)
```
_Source: source/src/pymatgen/analysis/chemenv/coordination_environments/coordination_geometries.py:994_

_Source doc:_ Store all the reference "coordination geometries" (list with instances of the CoordinationGeometry classes).

### Goal
Instantiate an in-memory, dictionary-like registry that stores all reference coordination geometries used for chemical environment and local structure analysis.

### Parameters
_None._

### Input
No parameters are required to instantiate the full registry according to the authoritative API signature. The class relies on built-in, in-memory data representing standard chemical coordination environments (e.g., octahedral, tetrahedral) and does not require external files or network queries. 

*(Note: While the project's test suite demonstrates an undocumented `only_symbols` keyword argument to filter the registry during instantiation, it is not part of the authoritative public signature.)*

### Output
Returns an `AllCoordinationGeometries` instance (which inherits from `dict`). This object maps standard coordination geometry symbols (e.g., `"SH:13"`, `"HP:12"`) to their corresponding `CoordinationGeometry` class instances.

### Valid Call Patterns
```python
# Instantiate the full registry of coordination geometries
allcg = AllCoordinationGeometries()

# Example usage derived from the test suite:
# Retrieve a specific geometry using its Materials Project symbol
mp_symbol = "SH:13"
cg = allcg.get_geometry_from_mp_symbol(mp_symbol=mp_symbol)
```

### LLM Instruction Prompt
- When performing local environment or chemical environment analysis, instantiate `AllCoordinationGeometries()` without arguments to access the complete in-memory registry of reference coordination geometries. 
- Do not attempt to query the Materials Project REST API to retrieve standard coordination shapes; they are fully contained within this object.
- Remember that this class is part of the `pymatgen.analysis` namespace. Following the 2026 architectural split, it requires the full `pymatgen` package to be installed, as it is not included in the minimal `pymatgen-core` distribution.

### Prompt Snippet
```text
To access reference coordination geometries for chemical environment analysis in pymatgen, instantiate `allcg = AllCoordinationGeometries()`. It acts as a dictionary mapping geometry symbols (like "SH:13") to `CoordinationGeometry` objects. Do not query external databases for these reference shapes; they are provided in-memory.
```

### Common Failure Modes
- **Network Querying for Geometries:** Attempting to fetch reference coordination geometries via `pymatgen.ext` (Materials Project API). This violates project constraints and is unnecessary, as `AllCoordinationGeometries` provides them in-memory.
- **Missing Dependency (2026 Split):** Attempting to import or use this class when only `pymatgen-core` is installed. Because it is an analysis tool, it requires the full `pymatgen` installation.
- **Inventing Parameters:** Passing positional arguments to the constructor. The authoritative signature accepts no parameters.

### Fix Code Hint
```python
# INCORRECT: Attempting to pass positional arguments or fetch from an API
# allcg = AllCoordinationGeometries("octahedral")

# CORRECT: Instantiate without arguments to get the full in-memory dictionary
from pymatgen.analysis.chemenv.coordination_environments.coordination_geometries import AllCoordinationGeometries

allcg = AllCoordinationGeometries()
cg = allcg.get_geometry_from_mp_symbol(mp_symbol="SH:13")
```

## API Test: `AngleCutoffFloat`

### Signature
```python
class AngleCutoffFloat(float, StrategyOption)
```
_Source: source/src/pymatgen/analysis/chemenv/coordination_environments/chemenv_strategies.py:92_

_Source doc:_ Angle cutoff in a strategy.

### Goal
Represents a validated angle cutoff value used as an option in chemical environment coordination strategies.

### Parameters
_None._

### Input
A numeric float value representing the angle cutoff. **Precondition:** The value provided during instantiation must be strictly between 0 and 1 (inclusive). It can also accept a serialized dictionary representation via the `from_dict()` class method.

### Output
Returns `unspecified` — An instance of `AngleCutoffFloat` that behaves as a standard Python `float` but includes strategy option methods for serialization (e.g., `as_dict()`).

### Valid Call Patterns
```python
# Instantiate directly with a float between 0 and 1
ac1 = AngleCutoffFloat(0.3)

# Serialize to a dictionary
ac1_dict = ac1.as_dict()

# Reconstruct from a dictionary
ac2 = AngleCutoffFloat.from_dict(ac1_dict)
```

### LLM Instruction Prompt
- When instantiating `AngleCutoffFloat`, you MUST ensure the provided float value is between 0 and 1. 
- Do not pass values greater than 1 (e.g., do not pass degrees if a normalized value is expected).
- Use `.as_dict()` and `.from_dict()` for serialization and deserialization of the strategy option.

### Prompt Snippet
```text
Instantiate AngleCutoffFloat with a value between 0 and 1.
```

### Common Failure Modes
- **`ValueError: Angle cutoff should be between 0 and 1, got ...`**: Occurs when attempting to instantiate the class with a float value outside the allowed [0, 1] range (e.g., passing `1.2`).

### Fix Code Hint
```python
# BAD: Passing a value > 1
# cutoff = AngleCutoffFloat(1.2) 

# GOOD: Ensure the value is bounded between 0 and 1
cutoff = AngleCutoffFloat(0.3)
```

## API Test: `AngleNbSetWeight`

### Signature
```python
class AngleNbSetWeight(NbSetWeight)
```
_Source: source/src/pymatgen/analysis/chemenv/coordination_environments/chemenv_strategies.py:1396_

_Source doc:_ Weight of neighbors set based on the angle.

### Goal
Defines a weighting factor for a set of neighboring atoms based on their angles, used in chemical environment (chemenv) coordination environment analysis strategies.

### Parameters
_None._

### Input
The caller instantiates the class to configure an angle-based weighting strategy. While the formal signature lists no parameters, the project's test suite demonstrates initialization with an `aa` parameter (e.g., `aa=1` or `aa=0.5`). To compute the actual weight, the caller must invoke the `.weight()` method on the resulting instance, providing a neighbor set (`nb_set`) that contains an `angles` attribute (a list of floats) and a `structure_environments` object.

### Output
Returns `unspecified` — An instance of `AngleNbSetWeight` that evaluates to a float weight value when its `.weight()` method is called.

### Valid Call Patterns
```python
# Instantiate the weight object (test suite demonstrates 'aa' parameter usage)
angle_weight = AngleNbSetWeight(aa=1)

# Calculate the weight for a given neighbor set and structure environments
aw = angle_weight.weight(nb_set=fake_nb_set, structure_environments=dummy_se)
```

### LLM Instruction Prompt
- Use `AngleNbSetWeight` to define angle-based neighbor set weights in `pymatgen.analysis.chemenv` coordination environment strategies. 
- Initialize the class with the `aa` parameter as demonstrated in the test suite (e.g., `AngleNbSetWeight(aa=1)`).
- To compute the weight, call the `.weight(nb_set=..., structure_environments=...)` method on the instance. Ensure the `nb_set` object has an `angles` attribute populated with a list of floats.

### Prompt Snippet
```text
angle_weight = AngleNbSetWeight(aa=1)
aw = angle_weight.weight(nb_set=fake_nb_set, structure_environments=dummy_se)
```

### Common Failure Modes
- Calling `.weight()` with a `nb_set` object that lacks an `angles` attribute, or where `angles` is not a list of floats.
- Omitting the required `structure_environments` argument when calling the `.weight()` method.
- Attempting to use this class for core structure manipulation instead of its intended use within the `pymatgen.analysis.chemenv` namespace.

### Fix Code Hint
```python
# Ensure the nb_set has the required angles attribute before calculating weight
fake_nb_set.angles = [1.859, 2.622, 3.085]
angle_weight = AngleNbSetWeight(aa=1)
aw = angle_weight.weight(nb_set=fake_nb_set, structure_environments=dummy_se)
```

## API Test: `AqueousCorrection`

### Signature
```python
class AqueousCorrection(Correction)
```
_Source: source/src/pymatgen/analysis/compatibility/__init__.py:358_

_Source doc:_ This class implements aqueous phase compound corrections for elements and H2O. Used only by MITAqueousCompatibility.

### Goal
This class implements aqueous phase compound corrections for elements and H2O, and is intended exclusively for use by `MITAqueousCompatibility`.

### Parameters
_None._

### Input
No initialization parameters are required. The caller simply instantiates the class without arguments.

### Output
Returns `unspecified` — an instance of `AqueousCorrection` (a subclass of `Correction`) that encapsulates the aqueous phase corrections.

### Valid Call Patterns
```python
# Inferred from signature (no verified test suite or README example provided)
correction = AqueousCorrection()
```

### LLM Instruction Prompt
- Instantiate `AqueousCorrection` without any arguments.
- Recognize that this class is a specialized `Correction` subclass used only by `MITAqueousCompatibility`. Do not attempt to use it as a general-purpose correction object in other thermodynamic workflows.
- Do not invent parameters for the constructor.

### Prompt Snippet
```text
Use `AqueousCorrection()` with no arguments to create an aqueous phase compound correction object for elements and H2O. Note that it is designed solely for use by `MITAqueousCompatibility`.
```

### Common Failure Modes
- **Passing arguments to the constructor:** The `AqueousCorrection` class takes no parameters. Providing arguments will result in a `TypeError`.
- **Misapplication in workflows:** Attempting to use this correction class in general thermodynamic workflows outside of its intended `MITAqueousCompatibility` context.

### Fix Code Hint
```python
# WRONG: Passing arguments to the constructor
# correction = AqueousCorrection(element="O")

# CORRECT: Instantiate without arguments
correction = AqueousCorrection()
```

## API Test: `BatteryAnalyzer`

### Signature
```python
class BatteryAnalyzer
```
_Source: source/src/pymatgen/apps/battery/analyzer.py:24_

_Source doc:_ A suite of methods for starting with an oxidized structure and determining its potential as a battery.

### Goal
Initialize an analyzer to evaluate an oxidized crystal structure's potential and properties as a battery material.

### Parameters
_None._ *(Note: While the authoritative API facts list no named parameters, the project's test suite demonstrates initializing the class with two positional arguments: a structure and a working ion string).*

### Input
*   **`struct`** (positional argument 1): An in-memory `Structure` object (from `pymatgen.core`). 
    *   **CRITICAL PRECONDITION:** The structure *must* have oxidation states assigned before being passed to the analyzer.
*   **Working ion** (positional argument 2): A string representing the working ion of the battery (e.g., `"Li"` for Lithium-ion batteries).
*   **Constraints:** Do not query the Materials Project or other network services to obtain the structure; prefer small in-memory structures or repository test fixtures.

### Output
Returns `unspecified` — An initialized `BatteryAnalyzer` instance containing a suite of methods for battery potential analysis.

### Valid Call Patterns
```python
# Derived from the project's test suite
analyzer = BatteryAnalyzer(struct, "Li")
```

### LLM Instruction Prompt
- When instantiating `BatteryAnalyzer`, you must pass a `Structure` object and a string representing the working ion (e.g., `"Li"`) as positional arguments.
- **Precondition:** You must ensure the input `Structure` has oxidation states assigned prior to initialization.
- Do not use `pymatgen.ext` to fetch structures from the Materials Project over the network; use local in-memory structures.

### Prompt Snippet
```text
Initialize `BatteryAnalyzer(struct, "Li")` to evaluate a material's battery potential. Ensure `struct` has oxidation states assigned before calling, or it will raise a ValueError.
```

### Common Failure Modes
- **Missing Oxidation States:** Passing a `Structure` that does not have oxidation states assigned will cause the initialization to fail, raising a `ValueError` with the exact match: `"BatteryAnalyzer requires oxidation states assigned to structure"`.

### Fix Code Hint
```python
# Ensure the structure has oxidation states assigned before initialization
# (Assuming `struct` is a valid pymatgen Structure that has been prepared with oxidation states)
try:
    analyzer = BatteryAnalyzer(struct, "Li")
except ValueError as e:
    print(f"Failed to initialize analyzer: {e}")
    # Fix: Assign oxidation states to `struct` before passing it to BatteryAnalyzer
```

## API Test: `BondDissociationEnergies`

### Signature
```python
class BondDissociationEnergies(MSONable)
```
_Source: source/src/pymatgen/analysis/bond_dissociation.py:29_

_Source doc:_ Standard constructor for bond dissociation energies. All bonds in the principle molecule are looped through and their dissociation energies are calculated given the energies of the resulting fragments, or, in the case of a ring bond, from the energy of the molecule obtained from breaking the bond and opening the ring. This class should only be called after the energies of the optimized principle molecule and all relevant optimized fragments have been determined, either from quantum chemistry or elsewhere. It was written to provide the analysis after running an `atomate` fragmentation workflow.

### Goal
Calculates the bond dissociation energies for all bonds in a principle molecule using the pre-computed energies of the optimized molecule and its resulting fragments.

### Parameters
_None._

### Input
The caller must provide the principle molecule entry and a collection of its fragment entries as positional arguments (as demonstrated in the project's test suite). 
**Precondition:** The energies of the optimized principle molecule and all relevant optimized fragments *must* have already been determined (e.g., from quantum chemistry calculations or an `atomate` fragmentation workflow) prior to initialization. Do not query external network services (like the Materials Project) to obtain these energies; workflows must rely on local, in-memory data or repository test fixtures.

### Output
Returns `unspecified` — An instantiated `BondDissociationEnergies` object (which is `MSONable`). The calculated energies can be accessed via the `.bond_dissociation_energies` attribute, and the relevant entries via the `.filtered_entries` attribute.

### Valid Call Patterns
```python
# Derived from source/tests/analysis/test_bond_dissociation.py
BDE = BondDissociationEnergies(principle_entry, fragment_entries)

# Accessing the calculated results
entries_count = len(BDE.filtered_entries)
energies = BDE.bond_dissociation_energies
```

### LLM Instruction Prompt
- ALWAYS ensure that the energies of the principle molecule and all fragments have been pre-calculated before instantiating `BondDissociationEnergies`.
- Pass the principle molecule entry and the fragment entries as positional arguments (as shown in the test suite), even though the formal signature parameters are unlisted.
- Access the calculated results using the `.bond_dissociation_energies` and `.filtered_entries` attributes.
- NEVER attempt to query the Materials Project or other network services to fetch the fragment energies; rely on provided in-memory structures or local workflow outputs.

### Prompt Snippet
```text
`BondDissociationEnergies` calculates bond dissociation energies from pre-computed molecule and fragment energies. Instantiate with `(principle_entry, fragment_entries)` and access results via the `.bond_dissociation_energies` attribute. Must be called after energies are determined (e.g., via atomate).
```

### Common Failure Modes
- **Missing Pre-calculated Energies:** Passing raw, unoptimized `Molecule` objects instead of entry objects that contain the pre-calculated thermodynamic energies from quantum chemistry workflows.
- **Network Query Violations:** Attempting to fetch fragment energies dynamically via `pymatgen.ext` REST APIs instead of using local/in-memory workflow outputs.
- **Missing Arguments:** Failing to pass the principle and fragment arguments because the documented signature parameters list is empty.

### Fix Code Hint
```python
# WRONG: Passing raw molecules without pre-calculated energies
# BDE = BondDissociationEnergies(raw_molecule, raw_fragments)

# CORRECT: Pass entries that already contain optimized energies (e.g., from atomate)
BDE = BondDissociationEnergies(optimized_principle_entry, optimized_fragment_entries)
bde_dict = BDE.bond_dissociation_energies
```

## API Test: `BorgQueen`

### Signature
```python
class BorgQueen
```
_Source: source/src/pymatgen/apps/borg/queen.py:24_

_Source doc:_ The Borg Queen controls the drones to assimilate data in an entire directory tree. Uses multiprocessing to speed up things considerably. It also contains convenience methods to save and load data between sessions.

### Goal
Orchestrates data assimilation across directory trees using multiprocessing and specific parser "drones", with capabilities to save and load assimilated materials data between sessions.

### Parameters
_None._

### Input
Based on the authoritative test suite, initialization requires a drone object (e.g., `VaspToComputedEntryDrone`). It optionally accepts a directory path string to scan (e.g., `TEST_DIR`) and an integer for the number of multiprocessing workers (e.g., `1`). Data can also be loaded from a previously saved JSON file path via the `load_data(filepath)` method.

### Output
Returns `unspecified` — An initialized `BorgQueen` instance that manages the assimilation process and yields parsed data (such as computed entries with energy values) via the `get_data()` method.

### Valid Call Patterns
```python
# Pattern 1: Assimilate data from a directory tree using a drone and a specified number of workers
drone = VaspToComputedEntryDrone()
queen = BorgQueen(drone, TEST_DIR, 1)
data = queen.get_data()

# Pattern 2: Initialize with a drone and load previously assimilated data from a JSON file
drone = VaspToComputedEntryDrone()
queen = BorgQueen(drone)
queen.load_data(f"{TEST_DIR}/assimilated.json")
data = queen.get_data()
```

### LLM Instruction Prompt
- When batch-parsing materials simulation outputs (like VASP directories), instantiate a drone (e.g., `VaspToComputedEntryDrone`) and pass it to `BorgQueen`. 
- Use `BorgQueen(drone, directory_path, num_workers)` to assimilate a directory tree, or `BorgQueen(drone)` followed by `queen.load_data(json_path)` to load a previous session. 
- Retrieve results using `queen.get_data()`. 
- Adhere to project constraints: prefer running `BorgQueen` on small repository test fixtures rather than large, unconstrained directory scans. Do not invent methods outside of `get_data()` and `load_data()`.

### Prompt Snippet
```text
`class BorgQueen`: Orchestrates directory-wide data assimilation using multiprocessing and parser drones. Initialize with a drone (and optionally a directory and worker count). Use `.get_data()` to retrieve parsed entries or `.load_data(filepath)` to load from JSON.
```

### Common Failure Modes
- **Missing Drone Dependency:** Failing to instantiate and pass a valid drone (like `VaspToComputedEntryDrone`) as the first argument to `BorgQueen`.
- **File Not Found:** Attempting to call `load_data()` with a non-existent JSON file path.
- **Environment Constraints:** Attempting to scan massive directories in constrained environments instead of using small, in-memory structures or repository test fixtures.

### Fix Code Hint
```python
# Ensure the drone is instantiated first and passed to the Queen
drone = VaspToComputedEntryDrone()

# To load from an existing file instead of scanning:
queen = BorgQueen(drone)
queen.load_data("path/to/assimilated.json")

# Always retrieve the final parsed list via get_data()
entries = queen.get_data()
```

## API Test: `BornEffectiveCharge`

### Signature
```python
class BornEffectiveCharge
```
_Source: source/src/pymatgen/analysis/piezo_sensitivity.py:33_

_Source doc:_ This class describes the Nx3x3 born effective charge tensor.

### Goal
This class describes and encapsulates the Nx3x3 Born effective charge tensor for a given crystal structure, allowing for the evaluation of its properties and symmetry operations.

### Parameters
_None._

### Input
Although no parameters are formally listed in the API signature facts, the project's test suite demonstrates that instantiation requires three positional arguments:
1. A crystal structure (e.g., an in-memory `pymatgen.core.Structure` object).
2. An Nx3x3 Born effective charge (BEC) tensor array (typically a `numpy` array).
3. A collection of point operations associated with the structure.

*Preconditions & Constraints:* The input structure must be constructed in-memory or loaded from a local file (like a CIF or VASP output). You must not query the Materials Project or other network services via `pymatgen.ext` to obtain this structure. If you only need core objects like `Structure`, ensure you are importing from the `pymatgen-core` package (or `pymatgen.core` namespace) per the 2026 architectural split.

### Output
Returns `unspecified` — An instance of the `BornEffectiveCharge` class. Based on the test suite, this instance exposes the tensor via the `.bec` attribute and provides methods like `.get_BEC_operations()` to compute or retrieve the associated BEC operations (accessible via the `.BEC_operations` attribute).

### Valid Call Patterns
```python
# Derived from the project's test suite
bec = BornEffectiveCharge(self.piezo_struct, self.BEC, self.point_ops)

# Accessing the tensor and operations
tensor_array = bec.bec
bec.get_BEC_operations()
operations_array = bec.BEC_operations
```

### LLM Instruction Prompt
- When instantiating `BornEffectiveCharge`, you MUST provide three positional arguments (structure, BEC tensor, point operations) as demonstrated by the test suite, even though the class signature appears empty.
- The BEC tensor provided must be of shape Nx3x3.
- Do not use network calls (e.g., `MPRester`) to fetch the input structure; use small in-memory `Structure` objects or local repository test fixtures.

### Prompt Snippet
```text
To analyze a Born effective charge tensor, instantiate `BornEffectiveCharge(structure, bec_tensor, point_ops)`. Ensure the `bec_tensor` is an Nx3x3 array. Do not fetch the `structure` from external databases; construct it in-memory using `pymatgen.core.Structure`.
```

### Common Failure Modes
- **Missing Arguments:** Attempting to instantiate `BornEffectiveCharge()` without arguments will fail. You must pass the structure, the BEC tensor, and the point operations.
- **Invalid Tensor Dimensions:** Passing a BEC tensor that is not an Nx3x3 array, which violates the mathematical definition expected by the class.
- **Network Violations:** Attempting to dynamically download the input structure using `pymatgen.ext` instead of relying on local or in-memory data.

### Fix Code Hint
```python
# ERROR: bec = BornEffectiveCharge() # Fails due to missing arguments
# FIX: Provide the structure, the Nx3x3 tensor, and the point operations
bec = BornEffectiveCharge(local_structure, nx3x3_bec_array, point_operations)
bec.get_BEC_operations()
```

