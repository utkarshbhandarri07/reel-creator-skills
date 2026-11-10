"""Create an isolated Reel project. Existing destinations are never overwritten."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import venv
from pathlib import Path

def run(args, **kwargs):
    subprocess.run([str(a) for a in args], check=True, **kwargs)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--skip-deps', action='store_true', help='Files only; runtime remains incomplete')
    args = parser.parse_args()
    kit = Path(__file__).resolve().parents[1]
    project = args.project.resolve()
    if project.exists(): parser.error('Destination already exists; choose a new project folder')
    if project == kit or kit in project.parents: parser.error('Projects must be outside the installed kit')
    node, npm = shutil.which('node'), shutil.which('npm')
    if not node or not npm: parser.error('Node and npm must be available')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        parser.error('FFmpeg and FFprobe must be available on PATH')
    run([node, '-e', "if(typeof require('node:module').stripTypeScriptTypes !== 'function') process.exit(1)"])
    vendors = json.loads((kit/'vendor/sources.json').read_text())
    for name, entry in vendors.items():
        if hashlib.sha256((kit/'vendor'/name).read_bytes()).hexdigest() != entry['sha256']:
            parser.error(f'Vendored dependency failed integrity check: {name}')
    project.mkdir(parents=True)
    shutil.copytree(kit/'engine', project/'web')
    (project/'web/lib').mkdir()
    shutil.copy2(kit/'vendor/three.module.js', project/'web/lib/three.module.js')
    for file in (kit/'tools').iterdir():
        if file.is_file() and file.suffix in {'.py', '.mjs', '.txt'} and file.name != 'setup.py':
            shutil.copy2(file, project/file.name)
    shutil.copy2(kit/'example/soldier/story.js', project/'web/story.js')
    shutil.copy2(kit/'example/soldier/audio.py', project/'audio.py')
    transform = "const fs=require('node:fs'),m=require('node:module');fs.writeFileSync(process.argv[2],m.stripTypeScriptTypes(fs.readFileSync(process.argv[1],'utf8'),{mode:'transform'}))"
    run([node, '-e', transform, kit/'vendor/toon.ts', project/'web/toonbase.js'])
    (project/'web/toon.js').write_bytes((project/'web/toonbase.js').read_bytes()+b'\n'+(project/'web/roman.js').read_bytes())
    (project/'package.json').write_text(json.dumps({'name':'reel-project','private':True,'type':'module','dependencies':{'playwright':'1.65.0'}},indent=2)+'\n')
    for folder in ['work','stills','out']: (project/folder).mkdir()
    metadata={'kit':str(kit),'runtime_ready':False,'example':'technical soldier demonstration; not verified history'}
    (project/'project.json').write_text(json.dumps(metadata,indent=2)+'\n')
    if not args.skip_deps:
        venv.create(project/'.venv', with_pip=True)
        py = project/'.venv'/('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
        run([py, '-m', 'pip', 'install', '-r', project/'requirements.txt'])
        run([npm, 'install', '--no-audit', '--no-fund'], cwd=project)
        run([node, project/'node_modules/playwright/cli.js', 'install', 'chromium'], cwd=project)
        run([py, '-c', 'import numpy,PIL,yaml'])
        metadata['runtime_ready']=True
        (project/'project.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(project)

if __name__ == '__main__': main()
