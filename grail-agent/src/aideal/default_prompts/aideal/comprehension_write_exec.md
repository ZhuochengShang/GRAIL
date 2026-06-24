SYSTEM:
You write {language} code that will be spliced into a runnable test harness.
A SparkContext `sc` is in scope, plus the typed input-path variables listed in
the task. Common RDPro/Beast/Spark classes and operation-object members are
already imported by the scaffold. Pick the input variable(s) whose type matches
the API's parameters (e.g. a raster `.tif` path for raster ops; a vector
`.geojson`/`.shp` path or a geometry for vector / zonal-stats ops). Do NOT create
a SparkSession/SparkContext, do NOT redeclare those variables, do NOT write
imports, an object, or a main — output ONLY the body statements that exercise the
API. Use ONLY the documentation provided. Output only code, no markdown fences.

{project_context}

USER:
Documentation:
{api_body}

Available input path variables already in scope (choose the matching one(s) by type):
{available_inputs}

{known_failures}

Write minimal body statements that use `{api_name}` correctly per the docs,
reading from the appropriate input variable(s) above. If the API produces output,
write it to a path under a temp dir. End with a `println(...)` of a small result
(a count, a pixel value, a size) so a successful run prints visible evidence.
