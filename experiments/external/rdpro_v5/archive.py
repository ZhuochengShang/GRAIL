"""Commit this study's evidence only after its single stage writer has exited."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

from .report import render


def archive(root, out, stage):
    wt=root.parents[1]
    render(root,out,'Completed stage: '+stage)
    target=root/'docs/main_v5/completed'/stage
    target.mkdir(parents=True,exist_ok=True)
    for name in ('status.json','index.html'):
        shutil.copy2(out/name,target/name)
    if stage=='feedback':
        shutil.copytree(out/'feedback',target/'feedback',dirs_exist_ok=True)
    elif stage in ('repair','B2'):
        source=root.parents[2]/'AIDEAL_rdpro_v5_B2/project/docs/main_v5'
        for name in ('docfix.json','LLM_readme.md','B2.json'):
            if (source/name).exists():
                shutil.copy2(source/name,target/name)
    subprocess.run(['git','add','--','experiments/rdpro/docs/main_v5'],cwd=wt,check=True)
    if subprocess.run(['git','diff','--cached','--quiet'],cwd=wt).returncode:
        subprocess.run(['git','commit','-m','Preserve RDPro main-v5 '+stage+' evidence'],cwd=wt,check=True)
    subprocess.run(['git','push','-u','origin','HEAD'],cwd=wt,check=True)


if __name__=='__main__':
    archive(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
