# SQLQueryHelper

_`extractTables` analyzes an SQL query to determine its syntactical correctness and retrieves the names of the tables referenced in the query._

**Receiver:** static object — call `SQLQueryHelper.<method>(...)`

**Members** (most robust first): ⚠️ `extractTables` **(primary)**

---

## API Test: `extractTables`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def extractTables(sql: String): Set[String]
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/SQLQueryHelper.scala:22_

_Source doc:_ Checks if an SQL query is syntactically correct and extracts table names from it. @param sql The SQL query string to be analyzed. @return Either an error message as a string if the query is incorrect, or a set of table names if the query is correct.

### Goal
`extractTables` analyzes an SQL query to determine its syntactical correctness and retrieves the names of the tables referenced in the query.

### Parameters
- `sql` (`String`): The SQL query string to be analyzed, which should follow standard SQL syntax.

### Input
The caller must provide a valid SQL query string. The query should be syntactically correct; otherwise, an error will be raised. 

### Output
Returns `Set[String]` — a set of table names extracted from the provided SQL query if it is correct. If the query is incorrect, an error message will be returned instead.

### Valid Call Patterns
```scala
val validSQL = "SELECT * FROM users"
val tables: Set[String] = SQLQueryHelper.extractTables(validSQL)
```

### LLM Instruction Prompt
- Ensure that the SQL query provided is syntactically correct before calling `extractTables`. If the query is invalid, handle the potential `SqlParseException`.

### Prompt Snippet
```text
Extract table names from the SQL query: "SELECT * FROM users".
```

### Common Failure Modes
- **[runtime]** java.lang.NoClassDefFoundError: org/apache/calcite/sql/util/SqlVisitor _(seen 3x)_
- **[compile]** error: not found: type SqlParseException

### Fix Code Hint
```scala
// Ensure the SQL query is valid before calling extractTables
val sqlQuery = "SELECT * FROM users"
try {
  val tables = SQLQueryHelper.extractTables(sqlQuery)
} catch {
  case e: SqlParseException => println(s"Error parsing SQL: ${e.getMessage}")
}
```
