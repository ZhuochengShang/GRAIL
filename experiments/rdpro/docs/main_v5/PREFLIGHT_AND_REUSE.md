# RDPro v5 registration and preflight

The generated README reproduces historical A2's delivered-document hash. We
reuse that document, not historical outcomes. A fresh A2 is necessary because
July's result lacks fingerprint components and retained builds point at another
modified source revision. Historical fix5 also regenerated its own round zero.

New source is clean Beast 547f7f912131a8032f6b5d26991415a5faf05cef. The primary
manifest is its deterministic 161-name public surface: 88 originally documented,
73 undocumented. The historical 10 generated extras remain excluded. No new A1
or original-document repair is scheduled; historical A1 is not a matched control
for this new runtime.

## Controlled preflight/fix attempts (not Gemini repair rounds)

1. Offline Maven package/tests inside the sandbox: local sockets blocked; five
   common-module errors. Retained build.log.
2. Same pinned build/tests outside the sandbox: exit 0. Seven module summaries
   total 832 tests, zero failures/errors/skips. Retained build_unrestricted.log.
3. Package the same source with Maven's uberjar profile after tests passed;
   -DskipTests avoids repeating the completed suite. Packaging exit 0.
4. Preflight dependency lookup found TIFF 1.4.14 in the local Ivy cache rather
   than Maven cache. The adapter now checks both exact coordinate paths.
5. The first executing smoke exposed inherited SPARK_HOME pointing to Spark
   3.3.1 despite compiling against the configured Spark 3.5.1. This produced a
   protobuf VerifyError. SPARK_HOME is now explicit in YAML and job environment.
6. The next smoke exposed unshaded Jetty dependencies used by Beast's CRS server.
   Add Jetty server/servlet 9.4.43 and place the newly built uberjar on the runtime
   classpath. Declared direct dependencies also enter the compiler classpath.
7. Final smoke passed: nonempty GeoTIFF tiles, nonempty shapefile features and
   geometry, shared SparkSession/Context, and protobuf-backed empty vector layer.
   This fixed snippet makes no LLM calls and earns no experiment score.

The default scaffold's SparkSession was outside GeoJob.run scope, while the
prompt promised a `spark` binding. The new scaffold provides that binding and
uses local[2] to bound CPU demand. Source/library code is unchanged. Input data
are physical copies with retained historical hashes: Boston GeoTIFF, shapefile
and sidecars, and upstream HDF4. The upstream HDF4ReaderTest passed five tests;
the smoke itself checks TIFF/vector loading, not every format/API combination.

build_identity.json binds 552 input files and 19 built/runtime jars. The native
schema-4 results additionally bind execution config, source, scaffold, fixture,
prompt/profile, engine, interpreter inventory and provider transport policy.
The source POM builds against Spark 3.4.2; the measured local runtime is explicitly
Spark 3.5.1/Scala 2.12.18/Java 8. This is a new registered runtime, not July replay.

A2 failures feed two independent branches: B2-1 uses README/error-only snippet
fixes; B2-2 uses source/tests/errors to repair README with zero-fix validations.
Both budgets are five, stuck threshold two. The final repaired README gets a
fresh 161-API zero-fix B2. Every saved A2 failure stays in the cohort. Scheduling
is serial through a shared supplemental slot, after priority B2-1 jobs. Providers
can retry after a minimum 300-second cooldown; queue waits may be longer.

The live dashboard reports recorded, pass, execution-failure and unresolved
provider counts separately, plus repair counts and per-API timing. Native
acceptance is not independent semantic validation. Historical scores are kept
separate. Completion by September 9, 11AM is not guaranteed.
