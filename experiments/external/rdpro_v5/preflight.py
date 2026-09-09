"""No-LLM fixture execution and build provenance for the new RDPro study."""
from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import shutil
import sys
from unittest.mock import patch

from aideal.config import load_config
from aideal.doc_checks import comprehension_check, form_check, completeness_check
from experiments.external.recovery.engine import save
from experiments.external.recovery.validation import file_sha


def preflight(root):
    docs = root/'docs/main_v5'
    cfg = load_config(root/'configs/aideal.main_v5.yaml')
    # The caller must have recorded the actual Maven process exit, not inferred it from a log.
    build = json.loads((docs/'build_exit.json').read_text())
    if build['exit_code'] != 0:
        raise ValueError('Pinned upstream build/tests failed; no measured launch')
    revision = subprocess.check_output(['git','-C',str(root/'beast'),'rev-parse','HEAD'],text=True).strip()
    dirty = subprocess.check_output(['git','-C',str(root/'beast'),'status','--porcelain','--untracked-files=no'],text=True).strip()
    if revision != '547f7f912131a8032f6b5d26991415a5faf05cef' or dirty:
        raise ValueError('Pinned source was changed during build')
    jars = list((root/'beast/target/beast-0.10.1-bin/beast-0.10.1/lib').glob('*.jar'))
    uber = root/'beast/target/beast-uber-0.10.1.jar'
    if not jars or not uber.is_file():
        raise ValueError('Pinned build did not produce the expected distribution')
    runtime = root/'runtime-libs'
    runtime.mkdir(exist_ok=True)
    dependencies = []
    for coordinate in cfg.comprehension['execute']['packages']:
        group, name, version = coordinate.split(':')
        dependency = Path.home()/'.m2/repository'/group.replace('.', '/')/name/version/(name+'-'+version+'.jar')
        if not dependency.is_file():
            dependency = Path.home()/'.ivy2/cache'/group/name/'jars'/(name+'-'+version+'.jar')
        if not dependency.is_file():
            raise ValueError('Declared dependency missing from local Maven/Ivy cache: '+coordinate)
        dependencies.append(dependency)
    for source in jars+dependencies:
        target = runtime/source.name
        if target.exists() and file_sha(target) != file_sha(source):
            raise ValueError('Existing runtime jar differs; preserve and inspect: '+str(target))
        if not target.exists():
            shutil.copy2(source,target)
    jars = list(runtime.glob('*.jar'))
    current = deepcopy(cfg)
    current.error_log = docs/'smoke_error_log.jsonl'
    ex = current.comprehension['execute']
    attempt = len(list((root/'.aideal_exec').glob('smoke*'))) + 1
    ex['work_dir'] = f'.aideal_exec/smoke_{attempt}'
    ex['output_dir'] = f'.aideal_exec/smoke_{attempt}/output'
    code = '''val tileCount = rasterRDD.count()
val featureCount = featuresRDD.count()
require(tileCount > 0, "GeoTIFF fixture must contain tiles")
require(featureCount > 0, "Shapefile fixture must contain features")
require(featuresRDD.first().getGeometry.getNumPoints > 0, "Vector geometry must be nonempty")
require(spark.sparkContext eq sc, "SparkSession binding must use the same context")
val layer = new edu.ucr.cs.bdlab.davinci.VectorLayerBuilder(256, "preflight").build()
require(layer.getFeaturesCount == 0, "Protobuf compile/runtime linkage must work")
println("__CHECK__ data-smoke tiles=" + tileCount + " features=" + featureCount)
'''
    # This is deterministic harness preflight, not an audience outcome.
    with patch('aideal.llm.invoke_text', return_value=code):
        result = comprehension_check(current, api='geoTiff', execute=True, show_code=True,
            doc_source='aideal', doc_scope='relevant', class_context=False, max_fix_rounds=0,
            timeout_s=600, resume=False, manifest='docs/main_v5/api_manifest.json')
    save(docs/'smoke.json', {'kind':'deterministic harness validation; no LLM', 'native':result})
    if result.get('metrics',{}).get('geoTiff',{}).get('status') != 'pass':
        raise ValueError('Fixture smoke failed; inspect smoke.json, no paid launch')
    save(docs/'document_structure.json', {'form':form_check(cfg), 'completeness':completeness_check(cfg)})
    files = list((root/'beast').glob('**/src/**/*.scala')) + list((root/'beast').glob('**/src/**/*.java'))
    files += list((root/'fixtures').glob('*'))
    files += [root/'configs/aideal.main_v5.yaml', root/'configs/project_profile.yaml',
              root/'docs/api_test_scaffold.scala', docs/'LLM_readme.md', docs/'api_manifest.json']
    log = (docs/'build_unrestricted.log').read_text(errors='replace')
    totals = re.findall(r'^Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)\s*$',log,re.M)
    result = {'upstream_passed':True, 'smoke_passed':True, 'source_revision':revision,
        'upstream_module_summaries':totals, 'build_exit':build,
        'smoke_sha256':file_sha(docs/'smoke.json'), 'build_log_sha256':file_sha(docs/'build_unrestricted.log'),
        'artifacts':{str(f.relative_to(root)):file_sha(f) for f in jars+[uber]},
        'inputs':{str(f.relative_to(root)):file_sha(f) for f in files if f.is_file()},
        'limitations':['Smoke checks GeoTIFF and shapefile loading plus Spark bindings; API-specific fixture suitability still belongs to each recorded test.',
                       'Upstream build uses Spark 3.4.2; measured runtime is existing Spark 3.5.1 / Scala 2.12.18, verified by the smoke. Historical engine/runtime equivalence is not claimed.']}
    save(docs/'build_identity.json',result)
    return result


if __name__ == '__main__':
    print(json.dumps(preflight(Path(sys.argv[1]).resolve())))
