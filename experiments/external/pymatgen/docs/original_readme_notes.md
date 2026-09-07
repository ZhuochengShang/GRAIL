Here are the distilled factual notes derived from the provided `pymatgen` documentation, structured for README and API documentation generation.

### 1. Project purpose
Pymatgen (Python Materials Genomics) is a robust, open-source Python library designed for comprehensive materials analysis. It serves as the foundational analysis engine powering the Materials Project. The library is built for computational materials scientists, chemists, scientific Python developers, and coding agents to construct, transform, and analyze crystal structures and molecular representations. It facilitates higher-level scientific workflows, including thermodynamic calculations, phase stability analysis, and electronic-structure evaluations, while providing a complete system for handling periodic boundary conditions.

### 2. Main workflows
*   **Structure and Molecule Construction:** Building and transforming in-memory representations of materials using core data objects.
*   **Simulation I/O and Parsing:** Reading, writing, and parsing inputs and outputs from major electronic-structure codes and standard chemical file formats.
*   **Thermodynamic and Reaction Analysis:** Performing thermodynamic calculations and reaction analyses using dedicated entry and thermo data objects.
*   **Phase Stability Analysis:** Generating and evaluating phase diagrams and Pourbaix diagrams to determine material stability.
*   **Electronic Structure Analysis:** Extracting, parsing, and summarizing electronic structure outputs, specifically focusing on density of states (DOS) and band structure analyses.
*   **Advanced Material Characterization:** Analyzing local environments, surfaces, interfaces, defects, magnetism, piezoelectricity, and elasticity.
*   **External Database Integration:** Querying and integrating data from external materials databases via REST APIs (though network queries are constrained in certain environments).

### 3. Important APIs and usage patterns
The library is organized into specific namespaces, separating core data structures from higher-level analyses:
*   `pymatgen.core`: The foundational namespace re-exporting the core data objects. The exact class names used for representing materials are `Element`, `Site`, `Molecule`, `Structure`, `Composition`, and `Lattice`.
*   `pymatgen.analysis`: The namespace containing powerful analysis tools for generating phase diagrams, Pourbaix diagrams, and analyzing reactions, local environments, surfaces, interfaces, defects, magnetism, piezoelectricity, and elasticity.
*   `pymatgen.entries`: The namespace containing entry/thermo data objects specifically designed for thermodynamic and reaction calculations.
*   `pymatgen.ext`: The namespace handling external integrations, including the Materials Project REST API and other materials databases.
*   `pymatgen.apps` and `pymatgen.cli`: Namespaces providing end-user applications and a command-line interface for terminal-based workflows.

### 4. Inputs and file formats
The library supports extensive input/output parsing for major electronic structure codes and standard crystallographic formats. Explicitly supported formats and codes include:
*   VASP
*   ABINIT
*   CIF (Crystallographic Information File)
*   Gaussian
*   XYZ (XYZ file format)
*   VASP POTCAR files (requires specific environment setup)

### 5. Outputs and generated artifacts
*   In-memory `Structure`, `Molecule`, and `Lattice` objects.
*   Phase diagrams and Pourbaix diagrams.
*   Density of states (DOS) summaries.
*   Band structure analyses.
*   Generated VASP POTCAR files.

### 6. Configuration and environment assumptions
*   **Numerical Optimization:** The library assumes the presence of `numpy` and `scipy`. Many core numerical methods and coordinate manipulations are heavily optimized via vectorization using these libraries to ensure fast execution.
*   **POTCAR Configuration:** The generation of VASP POTCAR files assumes the user has performed additional, specific environment setup beyond a standard `pip` installation.
*   **Distribution:** The package is assumed to be installed via PyPI (`pip`) or Conda (`conda-forge`).

### 7. Commands and examples

**Full Installation (Analyses, Apps, and Core I/O):**
```sh
pip install pymatgen
```

**Minimal Installation (Core Objects and I/O Only):**
```sh
pip install pymatgen-core
```

*(Note: The source documentation does not provide any Python API code examples for constructing structures, parsing files, or running analyses. Only installation commands are provided.)*

### 8. Constraints, preconditions, compatibility rules, and type-selection rules
*   **2026 Architectural Split (CRITICAL COMPATIBILITY RULE):** The core data objects (`Element`, `Site`, `Molecule`, `Structure`, `Composition`, `Lattice`) and file I/O for major electronic structure codes have been permanently moved to a lean, standalone package named `pymatgen-core`.
*   **Dependency Rule:** Installing the main `pymatgen` package automatically pulls in `pymatgen-core` as a dependency and re-exports its classes under the `pymatgen.core` namespace. 
*   **Type-Selection/Installation Constraint:** If a downstream application or user *only* requires the core data objects and file I/O capabilities, they must depend on `pymatgen-core` directly to ensure a much lighter installation footprint.
*   **Precondition for POTCARs:** The generation of POTCARs is not valid out-of-the-box; it requires additional setup before the operation can be executed.
*   **Network Constraint:** Do not query the Materials Project or other network services via `pymatgen.ext`. Workflows must prefer small in-memory structures and repository test fixtures.

### 9. Facts to preserve in the final README
*   Pymatgen is the primary analysis code powering the well-established Materials Project.
*   The library includes a complete, built-in system for handling periodic boundary conditions.
*   Coordinate manipulations are exceptionally fast due to `numpy`/`scipy` vectorization.
*   The project operates under a shared copyright model among the Pymatgen Development Team.
*   The software is released under the MIT License.
*   Primary citation: Ong et al., *Computational Materials Science*, 2013, 68, 314-319 (doi:10.1016/j.commatsci.2012.10.028).

### 10. Missing or weak documentation
*   **Not clearly documented:** There are absolutely no Python code examples demonstrating how to instantiate core objects like `Structure`, `Molecule`, or `Lattice`.
*   **Not clearly documented:** The exact class names, method signatures, and initialization parameters within `pymatgen.analysis`, `pymatgen.entries`, and `pymatgen.ext` are entirely missing. The documentation only provides high-level namespace descriptions.
*   **Not clearly documented:** The specific steps required for the "additional setup" to generate POTCARs are omitted.
*   **Not clearly documented:** There are no type-parameter selection rules, generic-type tables, or specific input/output type mappings provided for any of the analysis workflows.
*   **Not clearly documented:** The exact usage, commands, and arguments for the command-line interface (`pymatgen.cli`) are not explained.