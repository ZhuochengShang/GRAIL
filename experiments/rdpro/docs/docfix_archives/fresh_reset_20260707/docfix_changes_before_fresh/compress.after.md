## API Test: `compress`
_Grounding: doc-repaired from source (docfix)._

### Goal
Invoke `MemoryTile.compress` to gzip-compress tile data **in place**. This is an internal mutating method (`Unit`), not a public end-user RDPro pipeline API.

### Valid Call Patterns|Valid Access Patterns
```scala
package edu.ucr.cs.bdlab.raptor

import edu.ucr.cs.bdlab.raptor.MemoryTile

val tile: MemoryTile = ???   // must be MemoryTile
tile.compress                // protected[raptor] method, no args, returns Unit
```

Access requirement (compile-time): `compress` is declared `protected[raptor]`, so this call is only legal from code in package `edu.ucr.cs.bdlab.raptor` (or compatible subclass context). Calling from arbitrary external package code fails access checks.

### LLM Instruction Prompt
Use `tile.compress` only when:
1) `tile` is `edu.ucr.cs.bdlab.raptor.MemoryTile`, and  
2) caller code is inside `package edu.ucr.cs.bdlab.raptor` (or valid subclass scope).

Do not document or generate this as a general public API for user pipelines. It mutates internal state and returns `Unit`.

### Prompt Snippet
```text
Place code under package edu.ucr.cs.bdlab.raptor.
Given val tile: MemoryTile, call:
tile.compress
No parameters, no return value capture.
```

### Common Failure Modes
- **Most likely failure**: compile-time access error by calling `tile.compress` from outside `edu.ucr.cs.bdlab.raptor` (method is `protected[raptor]`).
- Calling it on a non-`MemoryTile` type.
- Treating it as public raster export/compression API (it does not take file/path arguments).

### Fix Code Hint
```scala
// Wrong (outside allowed package; will not compile)
package my.app
val tile: edu.ucr.cs.bdlab.raptor.MemoryTile = ???
tile.compress

// Correct (inside allowed package scope)
package edu.ucr.cs.bdlab.raptor
val tile: MemoryTile = ???
tile.compress
```