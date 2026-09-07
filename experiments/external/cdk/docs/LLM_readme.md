# CDK — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `AcidicGroupCountDescriptor`

### Signature
```java
public AcidicGroupCountDescriptor()
```
_Source: source/descriptor/qsarmolecular/src/main/java/org/openscience/cdk/qsar/descriptors/molecular/AcidicGroupCountDescriptor.java:60_

_Source doc:_ Creates a new {@link AcidicGroupCountDescriptor}.

### Goal
Creates a new instance of `AcidicGroupCountDescriptor` for calculating the number of acidic groups in a chemical structure as a Quantitative Structure-Activity Relationship (QSAR) molecular descriptor.

### Parameters
_None._

### Input
No arguments are required for instantiation. The resulting descriptor object is intended to be subsequently evaluated against small in-memory molecular object models (e.g., parsed from SMILES, SDF, or CML formats) using the public `org.openscience.cdk` APIs.

### Output
Returns `null` (constructor) — a newly instantiated `AcidicGroupCountDescriptor` object ready to process chemical structures.

### Valid Call Patterns
```java
// Instantiate the QSAR descriptor using the no-argument constructor
AcidicGroupCountDescriptor descriptor = new AcidicGroupCountDescriptor();
Assertions.assertNotNull(descriptor);
```

### LLM Instruction Prompt
- To calculate the acidic group count QSAR descriptor, instantiate the class using its no-argument constructor `new AcidicGroupCountDescriptor()`. Do not attempt to pass molecules or configuration parameters during instantiation.

### Prompt Snippet
```text
Instantiate the descriptor with `new AcidicGroupCountDescriptor()` before applying it to an in-memory molecule to calculate its QSAR properties.
```

### Common Failure Modes
- **Passing arguments to the constructor:** The constructor takes no parameters. Attempting to pass an `IAtomContainer` or configuration string directly into `new AcidicGroupCountDescriptor(...)` will cause a compilation error.
- **Missing Classpath Dependencies:** Failing to include the specific CDK QSAR molecular descriptor module (or the `cdk-bundle`) in the Maven `pom.xml` or Java classpath, resulting in a `ClassNotFoundException`.
- **Unsupported Environments:** Attempting to run the code on a Java Runtime Environment older than version 1.7.

### Fix Code Hint
```java
// Incorrect: new AcidicGroupCountDescriptor(molecule);
// Correct: Instantiate first, then evaluate
AcidicGroupCountDescriptor descriptor = new AcidicGroupCountDescriptor();
```

## API Test: `AminoAcid`

### Signature
```java
public AminoAcid()
```
_Source: source/base/data/src/main/java/org/openscience/cdk/AminoAcid.java:59  (+1 more definition site/overload)_

_Source doc:_ Constructs a new AminoAcid.

### Goal
Constructs a new, empty in-memory representation of an amino acid within the CDK molecular object model.

### Parameters
_None._

### Input
No arguments are required. The caller must ensure a Java 1.7+ runtime environment and that the CDK library (either the specific module or the `cdk-bundle` uber JAR) is explicitly included on the Java classpath.

### Output
Returns `unspecified` — an instance of `AminoAcid` (typically assigned to the `IAminoAcid` interface) representing an empty in-memory amino acid structure ready to be populated with atoms, bonds, and properties.

### Valid Call Patterns
```java
// Instantiate an empty amino acid and assign it to the IAminoAcid interface
IAminoAcid oAminoAcid = new AminoAcid();
Assertions.assertNotNull(oAminoAcid);
```

### LLM Instruction Prompt
- Use the no-argument constructor `new AminoAcid()` to instantiate an empty amino acid object.
- Assign the resulting instance to the `org.openscience.cdk.interfaces.IAminoAcid` interface, as is standard practice in the CDK object model.
- Do not attempt to pass chemical strings (like SMILES), file paths, or amino acid names (e.g., "Alanine") to this constructor; it takes no parameters.

### Prompt Snippet
```text
// Construct a new AminoAcid object in memory
IAminoAcid oAminoAcid = new AminoAcid();
```

### Common Failure Modes
- **Passing arguments to the constructor:** Attempting to initialize the amino acid by passing a SMILES string, InChI, or common name directly into `new AminoAcid(...)`. The constructor takes no arguments; parsing strings requires separate CDK reader or parser classes.
- **Classpath errors (`NoClassDefFoundError`):** Failing to include the CDK JARs on the classpath when compiling or running the Java application.
- **Type assignment issues:** Assigning the result to an incompatible interface or failing to import `org.openscience.cdk.interfaces.IAminoAcid`.

### Fix Code Hint
```java
// INCORRECT: IAminoAcid aa = new AminoAcid("C(C(C(=O)O)N)S"); // Constructor takes no arguments

// CORRECT:
IAminoAcid oAminoAcid = new AminoAcid();
// (Further configuration or atom/bond additions would follow using CDK APIs)
```

## API Test: `Aromaticity`

### Signature
```java
public Aromaticity(ElectronDonation model, CycleFinder cycles)
```
_Source: source/base/standard/src/main/java/org/openscience/cdk/aromaticity/Aromaticity.java:235_

_Source doc:_ Create an aromaticity model using the specified electron donation {@code model} which is tested on the {@code cycles}. The {@code model} defines how many π-electrons each atom may contribute to an aromatic system. The {@code cycles} defines the {@link CycleFinder} which is used to find cycles in a molecule. The total electron donation from each atom in each cycle is counted and checked. If the electron contribution is equal to {@code 4n + 2} for a {@code n >= 0} then the cycle is considered aromatic.  Changing the electron contribution model or which cycles are tested affects which atoms/bonds are found to be aromatic. There are several {@link ElectronDonation} models and {@link org.openscience.cdk.graph.Cycles} available. A good choice for the cycles is to use {@link org.openscience.cdk.graph.Cycles#all()} falling back to {@link org.openscience.cdk.graph.Cycles#relevant()} on failure. Finding all cycles is very fast but may produce an exponential number of cycles. It is therefore not feasible for complex fused systems and an exception is thrown. In such cases the aromaticity can either be skipped or a simpler polynomial cycle set {@link org.openscience.cdk.graph.Cycles#relevant()} used. <blockquote><pre> // mimics the CDKHuckelAromaticityDetector Aromaticity aromaticity = new Aromaticity(ElectronDonation.cdk(), Cycles.cdkAromaticSet()); // mimics the DoubleBondAcceptingAromaticityDetector Aromaticity aromaticity = new Aromaticity(ElectronDonation.cdkAllowingExocyclic(), Cycles.cdkAromaticSet()); // a good model for writing SMILES Aromaticity aromaticity = new Aromaticity(ElectronDonation.daylight(), Cycles.all()); // a good model for writing MDL/Mol2 Aromaticity aromaticity = new Aromaticity(ElectronDonation.piBonds(), Cycles.all()); </pre></blockquote> @param model the model @param cycles the cycles to apply it to @see ElectronDonation @see org.openscience.cdk.graph.Cycles

### Goal
Create an aromaticity model that perceives aromatic atoms and bonds in a molecule by checking if cycles satisfy the 4n + 2 π-electron rule according to a specific electron donation model and cycle-finding strategy.

### Parameters
- `model` (`ElectronDonation`): The model defining how many π-electrons each atom may contribute to an aromatic system (e.g., `ElectronDonation.daylight()`, `ElectronDonation.cdk()`, `ElectronDonation.piBonds()`).
- `cycles` (`CycleFinder`): The strategy used to find cycles in a molecule to test for aromaticity (e.g., `Cycles.all()`, `Cycles.cdkAromaticSet()`, `Cycles.relevant()`).

### Input
The caller must provide valid `ElectronDonation` and `CycleFinder` instances. The choice of these parameters depends on the downstream use case (e.g., writing SMILES vs. writing MDL/Mol2). The resulting `Aromaticity` instance is then applied to a small in-memory molecule (e.g., an `IAtomContainer` parsed from SMILES or an SDF file).

### Output
Returns `unspecified` — An instantiated `Aromaticity` object configured with the provided electron donation and cycle-finding models, which can subsequently be applied to a molecule to perceive its aromaticity.

### Valid Call Patterns
```java
// Standard usage for SMILES generation (from test suite and source docs)
Aromaticity aromaticity = new Aromaticity(ElectronDonation.daylight(), Cycles.all());
aromaticity.apply(mol);

// Usage mimicking the CDKHuckelAromaticityDetector
Aromaticity aromaticityHuckel = new Aromaticity(ElectronDonation.cdk(), Cycles.cdkAromaticSet());
aromaticityHuckel.apply(mol);

// Usage for writing MDL/Mol2 formats
Aromaticity aromaticityMol2 = new Aromaticity(ElectronDonation.piBonds(), Cycles.all());
aromaticityMol2.apply(mol);
```

### LLM Instruction Prompt
- When perceiving aromaticity, instantiate `Aromaticity` with the appropriate `ElectronDonation` and `Cycles` models for the target output format: use `ElectronDonation.daylight()` and `Cycles.all()` for SMILES, or `ElectronDonation.piBonds()` and `Cycles.all()` for MDL/Mol2.
- Always call `.apply(mol)` on the resulting `Aromaticity` instance to actually perform the perception on the `IAtomContainer`.
- Be aware that `Cycles.all()` can fail on complex fused systems by producing an exponential number of cycles; instruct the code to fall back to `Cycles.relevant()` if an exception is thrown.

### Prompt Snippet
```text
To perceive aromaticity on an IAtomContainer `mol` for SMILES output, initialize the model using `Aromaticity aromaticity = new Aromaticity(ElectronDonation.daylight(), Cycles.all());` and then execute `aromaticity.apply(mol);`. If processing complex fused ring systems, catch exceptions from `Cycles.all()` and fallback to `Cycles.relevant()`.
```

### Common Failure Modes
- **Exponential Cycle Explosion**: Using `Cycles.all()` on complex fused ring systems can produce an exponential number of cycles, making it unfeasible and causing an exception to be thrown.
- **Missing Application**: Instantiating the `Aromaticity` object but forgetting to call `.apply(mol)`, resulting in a molecule with unperceived aromaticity.
- **Mismatched Models**: Using an electron donation model that is incompatible with the intended output format (e.g., using the CDK model when Daylight SMILES output is expected), leading to incorrect aromaticity flags.

### Fix Code Hint
```java
Aromaticity aromaticity;
try {
    aromaticity = new Aromaticity(ElectronDonation.daylight(), Cycles.all());
    aromaticity.apply(mol);
} catch (Exception e) {
    // Fallback for complex fused systems where Cycles.all() is not feasible
    aromaticity = new Aromaticity(ElectronDonation.daylight(), Cycles.relevant());
    aromaticity.apply(mol);
}
```

## API Test: `AtomContainerAtomPermutor`

### Signature
```java
public AtomContainerAtomPermutor(IAtomContainer atomContainer)
```
_Source: source/base/standard/src/main/java/org/openscience/cdk/graph/AtomContainerAtomPermutor.java:52_

_Source doc:_ A permutor wraps the original atom container, and produces cloned (and permuted!) copies on demand. @param atomContainer the atom container to permute

### Goal
Creates an iterator-like permutor that wraps an original atom container to produce cloned copies of the molecule with permuted atom orderings on demand.

### Parameters
- `atomContainer` (`IAtomContainer`): The in-memory molecule (atom container) whose atoms are to be permuted.

### Input
An instantiated `IAtomContainer` representing a small in-memory molecule. Because permutations scale factorially with the number of atoms, the input molecule must be strictly small to avoid combinatorial explosion and out-of-memory errors. The molecule should be fully constructed (atoms and bonds added) before passing it to the permutor.

### Output
Returns `unspecified` — An `AtomContainerAtomPermutor` instance that acts as an iterator, yielding cloned `IAtomContainer` objects with permuted atom indices via its `next()` method.

### Valid Call Patterns
```java
// Example 1: Iterating through permutations to test fingerprint consistency
AtomContainerAtomPermutor acp = new AtomContainerAtomPermutor(pamine);
while (acp.hasNext()) {
    IAtomContainer container = acp.next();
    IBitFingerprint bs2 = fp.getBitFingerprint(container);
    Assertions.assertTrue(bs1.equals(bs2));
}

// Example 2: Iterating through permutations to test canonical SMILES generation
AtomContainerAtomPermutor acap = new AtomContainerAtomPermutor(mol);
while (acap.hasNext()) {
    IAtomContainer permutedMol = DefaultChemObjectBuilder.getInstance().newInstance(IAtomContainer.class, acap.next());
    String smiles = sg.create(permutedMol);
    Assertions.assertEquals(oldSmiles, smiles);
}
```

### LLM Instruction Prompt
- When testing canonical SMILES generation or fingerprint consistency, use `new AtomContainerAtomPermutor(atomContainer)` to generate all permutations of a molecule's atoms. Iterate through the permutations using `hasNext()` and `next()`. Ensure the input molecule is very small to prevent factorial time complexity from hanging the application.

### Prompt Snippet
```text
Use `new AtomContainerAtomPermutor(atomContainer)` to wrap an `IAtomContainer`. Iterate over it using `hasNext()` and `next()` to retrieve cloned `IAtomContainer` instances with permuted atom orderings. Restrict usage to small molecules.
```

### Common Failure Modes
- **Combinatorial Explosion**: Passing a large molecule (e.g., > 10-12 atoms) will result in factorial time complexity ($N!$ permutations), causing the application to hang or run out of memory.
- **NullPointerException**: Passing a `null` reference instead of a valid `IAtomContainer` will cause a failure upon instantiation or iteration.
- **Treating the Permutor as a Molecule**: Attempting to pass the `AtomContainerAtomPermutor` directly to a method expecting an `IAtomContainer` instead of calling `.next()` to extract the permuted copies.

### Fix Code Hint
```java
// Ensure the molecule is small to avoid combinatorial explosion
AtomContainerAtomPermutor permutor = new AtomContainerAtomPermutor(smallMolecule);
while (permutor.hasNext()) {
    // Extract the permuted copy
    IAtomContainer permutedCopy = permutor.next();
    
    // Use the permuted copy (e.g., for canonical SMILES or fingerprint testing)
    // String smiles = smilesGenerator.create(permutedCopy);
}
```

## API Test: `AtomContainerBondPermutor`

### Signature
```java
public AtomContainerBondPermutor(IAtomContainer atomContainer)
```
_Source: source/base/standard/src/main/java/org/openscience/cdk/graph/AtomContainerBondPermutor.java:54_

_Source doc:_ A permutor wraps the original atom container, and produces cloned (and permuted!) copies on demand. @param atomContainer the atom container to permute

### Goal
Wraps an original in-memory molecule (atom container) to produce cloned copies with permuted bonds on demand.

### Parameters
- `atomContainer` (`IAtomContainer`): The in-memory molecule whose bonds are to be permuted.

### Input
An instantiated `IAtomContainer` representing a small in-memory molecule, populated with atoms and bonds (e.g., created via `DefaultChemObjectBuilder.getInstance().newAtomContainer()`). 

### Output
Returns `unspecified` (Constructor) — A new `AtomContainerBondPermutor` instance. Based on test suite usage, this instance acts as an iterator providing `hasNext()` and `next()` methods to retrieve the cloned, permuted `IAtomContainer` copies.

### Valid Call Patterns
```java
// Example 1: Iterating through bond permutations to verify canonical SMILES generation
AtomContainerBondPermutor acbp = new AtomContainerBondPermutor(mol);
while (acbp.hasNext()) {
    IAtomContainer permuted = acbp.next();
    // Process the permuted clone (e.g., generate SMILES or fingerprints)
}

// Example 2: Iterating through permutations to verify fingerprint consistency
AtomContainerBondPermutor acp = new AtomContainerBondPermutor(pamine);
while (acp.hasNext()) {
    IAtomContainer container = acp.next();
    IBitFingerprint bs2 = fp.getBitFingerprint(container);
}
```

### LLM Instruction Prompt
- To generate bond permutations of a molecule, instantiate `AtomContainerBondPermutor` by passing the target `IAtomContainer`.
- Do not assume the original `IAtomContainer` is modified in place; the permutor produces cloned copies.
- Use a `while` loop with the `hasNext()` and `next()` methods on the resulting `AtomContainerBondPermutor` instance to retrieve each permuted `IAtomContainer`.
- Ensure operations are constrained to small in-memory molecules using public `org.openscience.cdk` APIs.

### Prompt Snippet
```text
Instantiate `AtomContainerBondPermutor` with an `IAtomContainer`. Iterate over the permutor using `hasNext()` and `next()` to retrieve cloned `IAtomContainer` instances with permuted bonds.
```

### Common Failure Modes
- **Modifying the original container**: Assuming the permutor modifies the input `IAtomContainer` in place rather than returning cloned copies via `next()`.
- **Missing iteration**: Instantiating the permutor but failing to call `hasNext()` and `next()` to actually retrieve the permuted molecules.
- **Null input**: Passing a null `IAtomContainer` to the constructor.

### Fix Code Hint
```java
// Correct usage: instantiate and iterate to get cloned copies
AtomContainerBondPermutor permutor = new AtomContainerBondPermutor(myAtomContainer);
while (permutor.hasNext()) {
    IAtomContainer permutedClone = permutor.next();
    // Use permutedClone safely here
}
```

## API Test: `AtomContainerSet`

### Signature
```java
public AtomContainerSet()
```
_Source: source/base/data/src/main/java/org/openscience/cdk/AtomContainerSet.java:70  (+1 more definition site/overload)_

_Source doc:_ Constructs an empty AtomContainerSet.

### Goal
Constructs an empty `AtomContainerSet` to hold a collection of in-memory molecular object models.

### Parameters
_None._

### Input
No arguments are required. The caller must be running Java 1.7 or higher and have the CDK library (either the `cdk-bundle` or specific modular dependencies) explicitly included on the Java classpath.

### Output
Returns `unspecified` — A new, empty `AtomContainerSet` instance (typically assigned to the `IAtomContainerSet` interface) that acts as a container for multiple chemical structures (`IAtomContainer` objects).

### Valid Call Patterns
```java
// Create an empty set and assign it to the IAtomContainerSet interface
IAtomContainerSet som = new AtomContainerSet();

// Example of adding a molecule to the set
IAtomContainer mol = DefaultChemObjectBuilder.getInstance().newAtomContainer();
som.addAtomContainer(mol);
```

### LLM Instruction Prompt
- When a collection of molecules is needed for cheminformatics workflows, instantiate `AtomContainerSet` using its no-argument constructor and assign it to the `IAtomContainerSet` interface. Do not pass any arguments to the constructor. Ensure operations remain constrained to small in-memory molecules.

### Prompt Snippet
```text
Use `IAtomContainerSet som = new AtomContainerSet();` to create an empty collection for in-memory molecules before adding `IAtomContainer` instances to it.
```

### Common Failure Modes
- **Passing arguments:** Attempting to pass an initial capacity or a collection to the constructor will fail to compile, as only the no-argument constructor is provided in the API facts.
- **Missing Classpath Dependencies:** Failing to include the CDK JAR files on the classpath, resulting in `ClassNotFoundException` or `NoClassDefFoundError`.
- **Environment Incompatibility:** Running on a Java version older than 1.7, which violates the strict precondition for compiling and running the library.
- **Out-of-Memory Errors:** Attempting to load massive external chemistry databases into the `AtomContainerSet` at once, violating the constraint to operate on small in-memory molecules.

### Fix Code Hint
```java
// Correct instantiation with no arguments, assigned to the interface
IAtomContainerSet som = new AtomContainerSet();
```

## API Test: `BasicGroupCountDescriptor`

### Signature
```java
public BasicGroupCountDescriptor()
```
_Source: source/descriptor/qsarmolecular/src/main/java/org/openscience/cdk/qsar/descriptors/molecular/BasicGroupCountDescriptor.java:57_

_Source doc:_ Creates a new {@link BasicGroupCountDescriptor}.

### Goal
Instantiates a new QSAR molecular descriptor calculator used to determine the number of basic groups within an in-memory chemical structure.

### Parameters
_None._

### Input
No arguments are required for instantiation. However, the caller must ensure the resulting descriptor instance is properly initialized before attempting to calculate descriptors for an `IAtomContainer` (molecule).

### Output
Returns `unspecified` — a new instance of `BasicGroupCountDescriptor`.

### Valid Call Patterns
```java
// Instantiate the descriptor
BasicGroupCountDescriptor descriptor = new BasicGroupCountDescriptor();
```

### LLM Instruction Prompt
- Use the no-argument constructor `new BasicGroupCountDescriptor()` to create the descriptor instance.
- **Crucial Precondition**: Do not chain or immediately call `.calculate(atomContainer)` on the newly created instance. The descriptor must be initialized first; otherwise, the calculation will fail. The specific initialization method is not provided in the current context, but it is a strict requirement.

### Prompt Snippet
```text
BasicGroupCountDescriptor descriptor = new BasicGroupCountDescriptor();
// Note: Descriptor must be initialized before calling .calculate()
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `.calculate(atomContainer)` is invoked on a newly instantiated `BasicGroupCountDescriptor` that has not yet been initialized.

### Fix Code Hint
```java
BasicGroupCountDescriptor descriptor = new BasicGroupCountDescriptor();
// Ensure the descriptor is initialized according to CDK QSAR requirements 
// before passing an IAtomContainer to its calculate() method.
```

## API Test: `BioPolymer`

### Signature
```java
public BioPolymer()
```
_Source: source/base/data/src/main/java/org/openscience/cdk/BioPolymer.java:63  (+1 more definition site/overload)_

_Source doc:_ Constructs a new Polymer to store the Strands.

### Goal
Constructs a new in-memory biological polymer object to store strands, monomers, and atoms.

### Parameters
_None._

### Input
No arguments are required for instantiation. The caller must ensure the execution environment is Java 1.7 or higher and that the CDK library (either the `cdk-bundle` or the specific required modules) is present on the Java classpath.

### Output
Returns `unspecified` — a new, empty `BioPolymer` instance (typically assigned to the `IBioPolymer` interface) with an initial monomer count of 0, ready to be populated with `IStrand`, `IMonomer`, and `IAtom` objects.

### Valid Call Patterns
```java
// Instantiate a new BioPolymer and assign it to the IBioPolymer interface
IBioPolymer oBioPolymer = new BioPolymer();

// The polymer is initially empty
assert oBioPolymer.getMonomerCount() == 0;
```

### LLM Instruction Prompt
- When tasked with creating a biological polymer representation in CDK, use the no-argument constructor `new BioPolymer()`.
- Always assign the resulting object to the `IBioPolymer` interface.
- Recognize that the newly constructed `BioPolymer` is completely empty; strands, monomers, and atoms must be instantiated (e.g., via `oBioPolymer.getBuilder().newInstance(...)`) and explicitly added to it.

### Prompt Snippet
```text
To initialize a biological polymer model in CDK, call `new BioPolymer()` and assign it to an `IBioPolymer` reference. The resulting object is an empty container designed to store `IStrand` and `IMonomer` components in memory.
```

### Common Failure Modes
- **`NoClassDefFoundError` or `ClassNotFoundException`**: Occurs if the CDK JAR files (e.g., `cdk-bundle` version 2.12) are not explicitly included on the Java classpath during compilation or execution.
- **UnsupportedClassVersionError**: Occurs if attempting to run the code on a Java Runtime Environment older than version 1.7, which is a strict precondition for the CDK.
- **Null Reference / Empty State Errors**: Assuming the `BioPolymer` comes pre-populated with default strands or atoms. Calling methods that expect existing data immediately after construction will fail or return empty results, as `getMonomerCount()` is initially 0.

### Fix Code Hint
```java
// Ensure proper imports are present
import org.openscience.cdk.BioPolymer;
import org.openscience.cdk.interfaces.IBioPolymer;

// Construct the polymer
IBioPolymer oBioPolymer = new BioPolymer();

// Note: You must build and add components (Strands, Monomers, Atoms) 
// before performing structural analysis.
```

## API Test: `BondCountDescriptor`

### Signature
```java
public BondCountDescriptor()
```
_Source: source/descriptor/qsarmolecular/src/main/java/org/openscience/cdk/qsar/descriptors/molecular/BondCountDescriptor.java:72_

_Source doc:_ Constructor for the BondCountDescriptor object

### Goal
Instantiates a QSAR molecular descriptor that calculates the total number of bonds in a given chemical structure.

### Parameters
_None._

### Input
The constructor takes no parameters. However, the resulting descriptor requires a valid, small in-memory `IAtomContainer` molecule (e.g., parsed from SMILES or SDF formats) when its `calculate` method is subsequently invoked.

### Output
Returns `unspecified` — an instance of `BondCountDescriptor` (which implements the `IMolecularDescriptor` interface). When its `calculate(IAtomContainer)` method is called, it yields a result whose value is an `IntegerResult` representing the bond count.

### Valid Call Patterns
```java
IMolecularDescriptor descriptor = new BondCountDescriptor();
IAtomContainer mol = sp.parseSmiles("CCO"); // ethanol
int bondCount = ((IntegerResult) descriptor.calculate(mol).getValue()).intValue();
```

### LLM Instruction Prompt
- Instantiate the descriptor using the no-argument constructor `new BondCountDescriptor()`.
- Assign the instance to the `IMolecularDescriptor` interface.
- To evaluate a molecule, call `calculate(IAtomContainer)` on the descriptor, call `getValue()` on the returned object, cast the value to `IntegerResult`, and extract the primitive integer using `.intValue()`.
- Ensure the input molecule is a parsed `IAtomContainer` object model, not a raw SMILES string.

### Prompt Snippet
```text
IMolecularDescriptor descriptor = new BondCountDescriptor();
int bondCount = ((IntegerResult) descriptor.calculate(mol).getValue()).intValue();
```

### Common Failure Modes
- **Missing Cast:** Failing to cast the generic result of `descriptor.calculate(mol).getValue()` to `IntegerResult` before attempting to read the integer value.
- **Invalid Input Type:** Attempting to pass string representations (like SMILES) directly to the descriptor's `calculate` method instead of first parsing them into an `IAtomContainer` object model using the CDK's public APIs.
- **Missing Classpath Dependencies:** Failing to include the CDK library (e.g., `cdk-bundle` version 2.12) on the Java 1.7+ classpath, resulting in `ClassNotFoundException`.

### Fix Code Hint
```java
// Incorrect: int count = descriptor.calculate(mol).getValue();
// Correct:
IMolecularDescriptor descriptor = new BondCountDescriptor();
IntegerResult result = (IntegerResult) descriptor.calculate(mol).getValue();
int bondCount = result.intValue();
```

## API Test: `Bspt`

### Signature
```java
public Bspt(int dimMax)
```
_Source: source/base/standard/src/main/java/org/openscience/cdk/graph/rebond/Bspt.java:92_

_Source doc:_ static double distance(int dim, Tuple t1, Tuple t2) { return Math.sqrt(distance2(dim, t1, t2)); } static double distance2(int dim, Tuple t1, Tuple t2) { double distance2 = 0.0; while (--dim >= 0) { double distT = t1.getDimValue(dim) - t2.getDimValue(dim); distance2 += distT*distT; } return distance2; }

### Goal
Initializes a Binary Space Partitioning Tree (BSPT) data structure to store and query spatial coordinates (tuples) up to a specified number of dimensions, typically used for distance calculations and rebonding atoms in 3D space.

### Parameters
- `dimMax` (`int`): The maximum number of spatial dimensions the tree will handle (e.g., `3` for 3D molecular coordinates).

### Input
An integer specifying the dimensionality of the space. 
*Preconditions:* The integer must be positive (typically 2 or 3 in cheminformatics contexts). The caller must ensure that any `Tuple` objects subsequently evaluated against this tree do not exceed this maximum dimensionality.

### Output
Returns a new `Bspt` instance representing an empty spatial partitioning tree ready to store and query multidimensional tuples.

### Valid Call Patterns
```java
// Initialize a BSPT for 3-dimensional space (e.g., 3D coordinates)
Bspt bspt = new Bspt(3);
```

### LLM Instruction Prompt
- When instantiating `Bspt`, provide the maximum number of dimensions as an integer (e.g., `3` for 3D space). 
- Use this data structure when performing spatial queries or Euclidean distance calculations between coordinates (like `Tuple` objects) during graph rebonding or coordinate analysis.
- Do not pass negative or zero values for `dimMax`.

### Prompt Snippet
```text
Use `new Bspt(3)` to initialize a spatial tree for 3D coordinate distance calculations and rebonding.
```

### Common Failure Modes
- **Invalid Dimensionality:** Providing a negative or zero dimension size, which will cause logical failures or out-of-bounds errors when the internal distance calculations iterate over the dimensions (e.g., `while (--dim >= 0)`).
- **Dimension Mismatch:** Attempting to evaluate `Tuple` objects that have fewer dimensions than the queried `dim` or `dimMax`, leading to errors when `getDimValue(dim)` is called.

### Fix Code Hint
```java
// Ensure dimMax matches the dimensionality of your molecular coordinates (usually 2 or 3)
int dimensions = 3; 
Bspt bspt = new Bspt(dimensions);
```

