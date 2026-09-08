# Thumbnailator: generated README failure review

Snapshot: 2026-09-07T23:23:08.290556-07:00

Open `AIDEAL_RESULTS_REVIEW.html` for charts, tables, an API inspector, fixtures, and a review queue. All assets and evidence are embedded; no server or internet connection is required.

## Readiness assessment

The frozen A2 result records 127 passes and 22 failures across 149 names. It is not a correctness-certified readiness score. The Java command does not enable assertions; all 127 passing snippets contain assertions. Three include unconditional `assert false` (IfdStructure, getBoolean, value). Isolated replays accept these snippets without -ea and reject all three with -ea. Native results remain unchanged.

Seven reviewed failures directly match incorrect guidance in the generated README. Seven fail on invented helper calls or wrong companion types in the audience test. Three concern receiver setup; three concern package-private APIs included in the frozen surface; two concern input/test assumptions. These are observed mechanisms, not controlled causal estimates of documentation impact or proof of 22 library defects.

## Attempted does not mean the target API ran

| A2 stage | Count | Interpretation |
|---|---:|---|
| API evaluation recorded | 149 | One final per-API outcome, including possible setup failures |
| Test code generated | 149 | Final A2 has no provider errors and no reused rows |
| Compiled and test process started | 135 | 14 tests stop at compilation |
| Runtime failures | 8 | Includes setup failures and post-target failures |
| Native recorded passes | 127 | Harness accepted exit status/markers with assertions disabled |
| Target API reached / correctness verified | Unknown overall | Requires target-call evidence and effective checks |

A timeout can end an evaluation before usable code exists. A compile failure means the API did not run. A runtime failure may occur before reaching the target. Calls inside disabled assertions are skipped. An API count counts distinct names; checkpoint-event counts also include repeated attempts and discarded fingerprint groups.

## Paired recorded outcomes

A1 is a changing checkpoint snapshot with explicit legacy compatibility; A2 is the completed native result. The original 127-versus-127 tie can change as A1 resolves provider outcomes. This snapshot uses the counts below rather than copying an earlier table.

- both_pass: 114
- a1_only: 14
- a2_only: 13
- neither_pass: 8

## Every A2 failure

| API | Native category | Primary reviewed mechanism | A1 snapshot |
|---|---|---|---|
| `Pipeline` | compile | documentation-contradiction | pass (no error) |
| `ThumbnailMaker` | compile | documentation-contradiction | fail (runtime) |
| `UnsupportedFormatException` | runtime | documentation-contradiction | pass (no error) |
| `clear` | compile | surface-accessibility | fail (llm-error) |
| `createOutputStream` | compile | surface-accessibility | fail (llm-error) |
| `defaultResizer` | runtime | receiver-setup | fail (runtime) |
| `defaultResizerFactory` | runtime | receiver-setup | pass (no error) |
| `filters` | compile | audience-helper-error | pass (no error) |
| `fitWithinDimenions` | runtime | receiver-setup | pass (no error) |
| `getDestination` | compile | documentation-contradiction | fail (compile) |
| `getExifOrientation` | runtime | input-and-test-assumption | fail (runtime) |
| `getFormatName` | runtime | documentation-contradiction | pass (no error) |
| `getInstance` | compile | audience-helper-error | pass (no error) |
| `getOrientationFromExif` | runtime | input-and-test-assumption | pass (no error) |
| `getOutputFormat` | runtime | documentation-contradiction | pass (no error) |
| `getRenderingHints` | compile | documentation-contradiction | pass (no error) |
| `getSourceRegion` | compile | audience-helper-error | fail (compile) |
| `init` | compile | surface-accessibility | pass (no error) |
| `quality` | compile | audience-helper-error | pass (no error) |
| `region` | compile | audience-helper-error | fail (llm-error) |
| `resizerFactory` | compile | audience-helper-error | pass (no error) |
| `setThumbnailParameter` | compile | audience-helper-error | pass (no error) |

### Pipeline

README repeatedly recommends new Rotation(90); generated test copies it. Rotation has a private no-argument constructor and exposes newRotator(double)/rotation constants, so the supporting expression cannot compile.

Input used: In-memory 120x60 ARGB BufferedImage and rotation filter

Proposed improvement: Replace invented constructors with Rotation.newRotator(90) or RIGHT_90_DEGREES and compile the complete Pipeline example.

Source evidence: `filters/Rotation.java:48`, `filters/Rotation.java:78`. Delivered entry SHA-256: `7f1c771bd0feda2a42eb9be228494c58d46a4edc256018f045c638bd089707a7`.

### ThumbnailMaker

README explicitly instructs new ThumbnailMaker(), copied by the test. ThumbnailMaker is abstract; its public constructor is not a directly instantiable API.

Input used: Receiver construction; no data file required

Proposed improvement: Preserve abstract/concrete class context and demonstrate a fully configured concrete maker or a subclass, rather than direct construction.

Source evidence: `makers/ThumbnailMaker.java:45`, `makers/ThumbnailMaker.java:179`. Delivered entry SHA-256: `3e211a3ade12c4aee1132019085d07dec34033e3a8ab93355a7cb868bab3cf33`.

### UnsupportedFormatException

Both constructor calls succeed in the snippet, but its extra pipeline test expects UnsupportedFormatException from outputFormat(superfakeformat). README recommends this exception flow; Builder.outputFormat instead immediately throws IllegalArgumentException.

Input used: Exception strings; extra test uses sourceImage and in-memory output stream

Proposed improvement: Separate testing the exception constructor from testing Builder validation. Document exception types at the actual call boundary.

Source evidence: `tasks/UnsupportedFormatException.java:70`, `Thumbnails.java:1661`. Delivered entry SHA-256: `510e7e8ad42526b1ab2b6d9a20cee6a73f5ddb0319b5b917b781132e3aaf4173`.

### clear

Frozen manifest contains package-private Configurations.clear(). README recommends a direct test call but omits the same-package access requirement; the external default-package harness cannot compile it.

Input used: Internal configuration state; no data file required

Proposed improvement: Review Java public-surface extraction and external accessibility. Keep current denominator frozen and identify this as ineligible for direct external calling; validate any corrected manifest in a new matched study.

Source evidence: `util/Configurations.java:130`. Delivered entry SHA-256: `b22fa95de6172a1da339fb0a1195832d751438c3bec8cb3cf84b2a2f38af1ce4`.

### createOutputStream

FileImageSink.createOutputStream(File) is package-private. The README's direct-call example is copied into an external harness and fails Java access checking before any file is opened.

Input used: Writable output File and four synthetic bytes; failure occurs before I/O

Proposed improvement: Separate test-only helpers from public APIs. Document supported public sink operations rather than bypassing access with reflection.

Source evidence: `tasks/io/FileImageSink.java:326`. Delivered entry SHA-256: `7580997a676fef64481a74ff1a468bcf7f5e06556e26d655c38b4ed5a91cbb93`.

### defaultResizer

The setter is called successfully, then make() fails because FixedSizeThumbnailMaker(50,50) leaves aspect-ratio and fit-within readiness unset. The delivered entry does not provide a complete receiver construction sequence.

Input used: 32x24 synthetic sourceImage and a 50x50 maker

Proposed improvement: Give a minimal fully initialized concrete receiver, including keepAspectRatio and fitWithinDimensions, and distinguish setter success from a subsequent make() failure.

Source evidence: `makers/FixedSizeThumbnailMaker.java:91`, `makers/FixedSizeThumbnailMaker.java:158`, `makers/ThumbnailMaker.java:195`. Delivered entry SHA-256: `f1ae03a849bd6d77a7449d07fe347175f9e7fd7ce9855d77cd7e0a4863e696b0`.

### defaultResizerFactory

Factory setter succeeds, but a subsequent make() runs on the same incompletely initialized two-argument FixedSizeThumbnailMaker. This is receiver lifecycle failure, not failure of the setter itself.

Input used: 32x24 synthetic sourceImage and a 50x50 maker

Proposed improvement: Provide an executable initialization sequence and show a state postcondition for the target setter.

Source evidence: `makers/FixedSizeThumbnailMaker.java:91`, `makers/FixedSizeThumbnailMaker.java:158`, `makers/ThumbnailMaker.java:290`. Delivered entry SHA-256: `7bd4f9cb42b204da50cbb8532d98b9221a44161b65c934425ef61cd3486b4559`.

### filters

The generated test uses nonexistent ThumbnailParameter.getFilters() to inspect the result; the real getter is getImageFilters(). The README does not tell the model to call getFilters(). It separately contains an invalid Rotation constructor, but that is not this observed compile error.

Input used: List containing Flip.HORIZONTAL and built ThumbnailParameter

Proposed improvement: Include the actual getter used to verify filters and compile the witness; repair the unrelated invalid Rotation example separately.

Source evidence: `ThumbnailParameter.java:919`, `builders/ThumbnailParameterBuilder.java:267`. Delivered entry SHA-256: `b433446b66bd851140bce5b1cb06d11fca4143ebc651d927d3886525d509c8ae`.

### fitWithinDimenions

README correctly preserves the misspelled method name, but supplies no complete parameter construction. The model uses reflection with guessed constructor arguments; a null Resizer triggers IllegalArgumentException before the target getter is reached.

Input used: Reflectively assembled constructor arguments, including invalid null Resizer

Proposed improvement: Provide a concrete valid ThumbnailParameterBuilder example and explicit non-null dependencies; discourage reflective constructor guessing.

Source evidence: `ThumbnailParameter.java:329`, `ThumbnailParameter.java:980`. Delivered entry SHA-256: `c784fd3def1d5c620f55f46a370f3ee0e200a04ee8f37ad040e08be490fc7b54`.

### getDestination

README conflates task.getDestination() with ImageSink operations. The test calls OutputStreamImageSink.getDestination(), which does not exist; sinks expose getSink().

Input used: ByteArrayOutputStream wrapped in OutputStreamImageSink

Proposed improvement: Separate receiver-qualified task and sink contracts; test getDestination on an actual task instead of substituting a sink method.

Source evidence: `tasks/ThumbnailTask.java:126`, `tasks/io/ImageSink.java:91`, `tasks/io/OutputStreamImageSink.java:268`. Delivered entry SHA-256: `6b6b2390803c0c7a14e06c2552d5a784e3838c7f7ed2c2c3cbf3fa7869a0cf52`.

### getExifOrientation

README correctly permits null and warns to handle it. Configured exif_jpeg points to Exif/original.jpg, whose orientation is null in the isolated probe. The test assumes a positive tag and dereferences orientation.name(); its preceding Java assert is disabled.

Input used: JPEG original.jpg has no orientation; orientation_6.jpg is a verified positive control

Proposed improvement: Use a checked-in tagged image for a positive orientation test and original.jpg for a separate null-return test. Validate fixture semantics and enable effective assertions in a reviewed matched harness revision.

Source evidence: `util/exif/ExifUtils.java:69`, `source/src/test/java/net/coobird/thumbnailator/util/exif/ExifUtilsTest.java:51`. Delivered entry SHA-256: `5497d2e076f4f2ed6c7c25d823060f37002ebfc69ad9b8a8015770faf3ba4622`.

### getFormatName

README leads the model to provoke an unsupported-format pipeline exception, but outputFormat() throws IllegalArgumentException before getFormatName() is reached.

Input used: Unsupported format string superfakeformat and synthetic sourceImage

Proposed improvement: Demonstrate new UnsupportedFormatException(format).getFormatName() for the getter contract and separately describe Builder validation exceptions.

Source evidence: `tasks/UnsupportedFormatException.java:80`, `Thumbnails.java:1661`. Delivered entry SHA-256: `64f3517a0218e982a6fd1c56ec6be90a67ab43d073ff2da4d022102271314576`.

### getInstance

Test invents net.coobird.thumbnailator.ThumbnailParameterBuilder. The actual class lives in net.coobird.thumbnailator.builders, already imported by the scaffold. The singleton methods are not the compile failure.

Input used: ResizerFactory singleton and parameter builder; no file data

Proposed improvement: Use the imported class or correct fully qualified name; include package-qualified companion types in documentation and validate supporting construction code.

Source evidence: `builders/ThumbnailParameterBuilder.java:25`, `resizers/DefaultResizerFactory.java:118`. Delivered entry SHA-256: `2533174cce0a253e39961983701e201837e65bf91ad7adf87310c1866510d6d4`.

### getOrientationFromExif

Retained full test source calls the parser on a three-byte array after its valid-data path. Source immediately reads four bytes, and the native stack identifies that call. The model wrongly generalizes no-orientation returns null into malformed/short data returns null.

Input used: JPEG APP1 extraction, generated valid Exif payload, then invalid three-byte array

Proposed improvement: Specify raw APP1 Exif payload structure and malformed-input behavior; provide validated bytes for a positive case and an explicitly expected exception for truncated input.

Source evidence: `util/exif/ExifUtils.java:109`. Delivered entry SHA-256: `52f065e1b85133a6a1a856cd57fb1cec600b9c2fcf0398cbd5360595d41891f1`.

### getOutputFormat

README recommends ThumbnailParameter.ORIGINAL_FORMAT.equals(format), but ORIGINAL_FORMAT is null. Test copies this pattern and throws NullPointerException after calling the target getter.

Input used: ThumbnailParameter configured with png plus default-format parameter

Proposed improvement: Document the null sentinel explicitly and use format == null or a null-safe comparison in every example.

Source evidence: `ThumbnailParameter.java:53`, `ThumbnailParameter.java:878`. Delivered entry SHA-256: `ce15ed07cc452f384cd144f071ddde19a0be6ab7591e4ac98faf44e978208d72`.

### getRenderingHints

README declares a receiver as Resizer and calls getRenderingHints(); the test copies it. That method belongs to AbstractResizer and is absent from the Resizer interface.

Input used: BicubicResizer object held through an incompatible interface type

Proposed improvement: Use an AbstractResizer or concrete BicubicResizer receiver and verify the static type in the example.

Source evidence: `resizers/AbstractResizer.java:146`, `resizers/Resizer.java:35`. Delivered entry SHA-256: `28da105f39dac558db542dd7aa2919f2747c20d75e60b6a889d6cb40df6ca2ae`.

### getSourceRegion

Target getter is not reached: test invents Region(Dimension), whereas Region requires Position and Size, and passes untyped null into overloaded ThumbnailParameter constructors, causing ambiguity.

Input used: Region geometry and ambiguous nullable constructor dependencies

Proposed improvement: Provide valid Region construction and a builder-based receiver example; verify helper signatures instead of guessing constructors.

Source evidence: `geometry/Region.java:59`, `ThumbnailParameter.java:967`. Delivered entry SHA-256: `3af37cfcf5ca8c9274610de139a167db7e8dedb66cc1fbc3ffdba836c4df52d0`.

### init

Configurations.init() is package-private. The README shows a direct call from a test, but being a test does not grant package access. The frozen external harness cannot compile it.

Input used: Configuration resource/classloader context; fails before loading

Proposed improvement: Audit external accessibility and distinguish package-local library tests from public consumer examples; do not change the active frozen denominator.

Source evidence: `util/Configurations.java:108`. Delivered entry SHA-256: `b589ab51df013f09e885735d7085cf292ae1a038898e7c053a2de8dc5f7b04e9`.

### quality

Test calls nonexistent ThumbnailParameter.getQuality(); the real getter is getOutputQuality(). The quality(float) call itself is not the compiler error.

Input used: Float 0.75f and a parameter builder

Proposed improvement: Include a checked getter-based postcondition using getOutputQuality and validate the full example.

Source evidence: `ThumbnailParameter.java:907`, `builders/ThumbnailParameterBuilder.java:232`. Delivered entry SHA-256: `d4980de33876d3a8a615a63a31866a46ea14b626eae59083b0c685b07b74ce8e`.

### region

Region setter and construction match README guidance, but the test invents a two-argument Region.calculate(100,100); the actual signature requires five arguments.

Input used: Coordinate(10,15), AbsoluteSize(50,60), and target size 20x20

Proposed improvement: Verify through identity or documented accessors, or include the exact five-argument helper contract when geometric calculation is required.

Source evidence: `geometry/Region.java:109`, `builders/ThumbnailParameterBuilder.java:200`. Delivered entry SHA-256: `df128464db70589d9f0d28d403056ea1535de36a829cf147c6396f72b349a698`.

### resizerFactory

The generated test uses the same nonexistent root-package ThumbnailParameterBuilder class as getInstance. README also conflates overload-specific restrictions, which needs separate review but is not the observed compiler error.

Input used: DefaultResizerFactory singleton, parameter builder and synthetic image

Proposed improvement: Correct the companion class identity and document contracts per declaring receiver rather than merging same-name methods into one rule.

Source evidence: `builders/ThumbnailParameterBuilder.java:25`, `Thumbnails.java:1348`. Delivered entry SHA-256: `dabc4ad34e07e707c50ebbe73fe5f7b8331017c930d497c2ae970c62c963c84d`.

### setThumbnailParameter

The model again places ThumbnailParameterBuilder in the root package. Compilation fails before source.setThumbnailParameter is executed.

Input used: BufferedImageSource over sourceImage, 5x5 Region, parameter builder

Proposed improvement: Use the correct builders package and supply a complete source/parameter construction example with a checked crop result.

Source evidence: `builders/ThumbnailParameterBuilder.java:25`, `tasks/io/AbstractImageSink.java:58`. Delivered entry SHA-256: `f8408049c322c5609b1924d530e783c0665856bc9d5449ba1bddc87e90fb673d`.

## Gemini timeout frequency

Separate snapshot: 2026-09-07T23:21:39.701725-07:00

| Cell | Timeout events / recorded evaluations | Percent |
|---|---:|---:|
| mir_eval_A1 | 125/243 | 51.4% |
| mir_eval_A2 | 0/149 | 0.0% |
| thumbnailator_A1 | 30/459 | 6.5% |
| thumbnailator_A2 | 1/298 | 0.3% |
| tslearn_A1 | 44/205 | 21.5% |
| tslearn_A2 | 14/1093 | 1.3% |

Counts include watchdog retries and historical fingerprint groups. They are not SDK request counts, independent function samples, or hourly rates. Most recorded provider failures take about 600 seconds. A1/A2 timing and documentation differ, so a lower A2 timeout rate does not establish a causal explanation. A provider outage is not a library defect.

## Safe fixes and remaining review

Implemented outside active measurement: compatibility-aware HTML counts, explicit stage labels, assertion/fixture diagnostic probes, and reporting-template validation requirements. The visual report uses 22 source- and document-bound reviews and supports local review decisions with JSON export.

Not changed in active runs: assertions, frozen API surface, fixture bindings, generated README, model, prompts, or budgets. Correcting those measurement settings in one condition would break comparability. A proposed matched validation revision is recorded separately; it is not an instruction to restart current workers.

The library developer queue should distinguish documentation correction, API usability improvements, and library behavior changes. Harness, manifest, and provider fixes belong to AIDEAL maintainers. Any source-informed diagnostic result stays separate from headline A1/A2/B1/B2 scores.

## Verification and limits

All 22 delivered README entry hashes match their native metric hashes. Source references exist and are embedded with file hashes. Contract probes confirm null ORIGINAL_FORMAT, missing EXIF in original.jpg, positive EXIF in orientation_6.jpg, maker readiness, wrong exception expectations, interface-method mismatch, and truncated-input behavior. Three native passing snippets were replayed only in temporary isolated classes with assertions off/on.

The DOM behavior test checks filters, all 149 API rows, paired totals, evidence inspector, local review decisions, and JSON/CSV exports. A browser was unavailable in this session, so visual rendering has not been inspected. The HTML is a timestamped snapshot and does not auto-refresh.
