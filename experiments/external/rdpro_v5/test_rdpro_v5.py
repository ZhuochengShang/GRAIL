import json
from pathlib import Path
import tempfile
import unittest

from experiments.external.rdpro_v5.worker import priority_ready, verify
from experiments.external.rdpro_v5.report import metrics


class RDProGuardTests(unittest.TestCase):
    def test_missing_build_blocks_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'before Gemini'):
                verify(Path(tmp))

    def test_all_priority_branches_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertFalse(priority_ready(root/'rdpro_v5'))
            for name in ('mir_eval','thumbnailator','tslearn'):
                folder = root/'main_plan_v5'/name
                folder.mkdir(parents=True)
                (folder/'summary.json').write_text(json.dumps({'complete':True}))
            self.assertTrue(priority_ready(root/'rdpro_v5'))
            (folder/'summary.json').write_text(json.dumps({'complete':False}))
            self.assertFalse(priority_ready(root/'rdpro_v5'))

    def test_missing_final_is_not_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows, state = metrics(Path(tmp),'A2')
            self.assertEqual(rows,{})
            self.assertIn('not a completed',state)

    def test_document_branch_receives_only_frozen_A2_failure(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        from experiments.external.rdpro_v5.worker import b2_project
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'workspace/wt/experiments/rdpro'
            docs = root/'docs/main_v5'
            docs.mkdir(parents=True)
            baseline = {'doc_source':'aideal', 'run':{'max_fix_rounds':0,
                'api_count':1,'manifest_api_count':1,'run_id':'new-A2'},
                'metrics':{'f':{'status':'fail','error_category':'compile','error':'actual A2 error'}}}
            (docs/'A2.json').write_text(json.dumps(baseline))
            (docs/'LLM_readme.md').write_text('frozen generated README')
            script=root/'.aideal_exec/A2/run_f/ApiTest.scala'
            script.parent.mkdir(parents=True)
            script.write_text('// start\nactual_failed_snippet()\n// end')
            (root/'logs').mkdir()
            (root/'logs/main_v5.jsonl').write_text('unrelated source diagnosis must not leak')
            cfg=SimpleNamespace(comprehension={'execute':{'work_dir':'.aideal_exec/A2',
                'test_filename':'ApiTest.scala','region':['// start','// end']}})
            with patch('experiments.external.rdpro_v5.worker.load_config',return_value=cfg):
                target=b2_project(root)
                self.assertEqual(b2_project(root),target)
            rows=(target/'logs/main_v5.jsonl').read_text().splitlines()
            self.assertEqual(len(rows),1)
            row=json.loads(rows[0])
            self.assertEqual(row['error'],'actual A2 error')
            self.assertIn('actual_failed_snippet()',row['code'])
            self.assertEqual((target/'docs/main_v5/LLM_readme.md').read_text(),'frozen generated README')
