## API Test: `using`

### Signature
```scala
def using[A <: AutoCloseable, B](resource: A)
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:606  (+1 more definition site/overload)_

### Goal
Safely run a block of code with an `AutoCloseable` resource (such as JDBC connections/statements/result sets) in Beast/RDPro workflows, ensuring the resource is scoped and then closed.

### Parameters
- `resource` (`A`): The open `AutoCloseable` instance to use inside the block (for example, `DriverManager.getConnection(...)`, `dbConnection.prepareStatement(...)`, `dbConnection.createStatement()`, or `statement.executeQuery(...)` as shown in tests).

### Input
A valid, already-created object of type `A <: AutoCloseable`, plus a function block (second parameter list, shown in tested usage) that receives that resource and performs work.

Preconditions from verified usage:
- The passed object must implement `AutoCloseable`.
- Resource creation must succeed before calling `using` (e.g., JDBC driver loaded, connection string valid).
- The tested/authoritative call form is a top-level `using(resource) { ... }` shape.

### Output
Returns `unspecified` — the provided API facts do not declare a concrete return type in this entry. From the generic signature, the helper is parameterized by `B`, so the block computes a value of that type, but exact documented return semantics are not specified in the provided source facts.

### Valid Call Patterns
```scala
using(DriverManager.getConnection(s"jdbc:h2:${datasetsPath}/beast", "sa", "")) {dbConnection =>
  DatasetProcessor.createDB(dbConnection)
  val insertSQL: String = "INSERT INTO datasets(name, dir_name, source_uri, source_format, status) VALUES (?, ?, ?, ?, ?)"
  using(dbConnection.prepareStatement(insertSQL)) { insertStatement =>
    insertStatement.setString(1, "cities")
    insertStatement.setString(2, "cities")
    insertStatement.setString(3, testData.getPath)
    insertStatement.setString(4, "shapefile")
    insertStatement.setString(5, "created")
    insertStatement.executeUpdate()
  }
}
```

```scala
using(dbConnection.createStatement()) { statement =>
  using(statement.executeQuery("SELECT * FROM datasets WHERE name='cities'")) { data =>
    assert(data.next())
    val status = data.getString("status")
    assertResult("ready")(status)
  }
}
```

### LLM Instruction Prompt
- Call it in the tested form: `using(resource) { r => ... }`.
- Pass only objects that are `AutoCloseable`.
- Nest `using` for dependent resources (connection → statement → result set).
- Do not invent alternate receiver forms unless present in project code.
- Ensure resource construction is done before `using(...)`.

### Prompt Snippet
```text
Use `using(resource) { r => ... }` with an `AutoCloseable` resource (e.g., JDBC Connection/PreparedStatement/ResultSet), and nest `using` blocks for child resources. Follow the exact tested call shape.
```

### Common Failure Modes
- Passing a non-`AutoCloseable` object as `resource` (type bound violation).
- Omitting the function block after `using(resource)`.
- Using an invalid/uninitialized JDBC resource (e.g., driver not loaded, bad URL) before entering `using`.
- Inventing undocumented call shapes (e.g., different receiver/qualifier form not shown in tests).

### Fix Code Hint
```scala
Class.forName("org.h2.Driver")

using(DriverManager.getConnection(s"jdbc:h2:${datasetsPath}/beast", "sa", "")) { dbConnection =>
  val insertSQL = "INSERT INTO datasets(name, dir_name, source_uri, source_format, status) VALUES (?, ?, ?, ?, ?)"
  using(dbConnection.prepareStatement(insertSQL)) { insertStatement =>
    insertStatement.setString(1, "cities")
    insertStatement.setString(2, "cities")
    insertStatement.setString(3, testData.getPath)
    insertStatement.setString(4, "shapefile")
    insertStatement.setString(5, "created")
    insertStatement.executeUpdate()
  }
}
```