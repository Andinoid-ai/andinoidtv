#!/usr/bin/env python3
"""Genera la carpeta publicable (GitHub Pages) de Andinoid TV.

Uso: python3 tools/build_repo.py --user GITHUB_USER [--repo andinoidtv] [--out docs]

Resultado (en --out):
  index.html                              <- lo que Kodi lista al añadir la fuente
  repository.andinoidtv-X.Y.Z.zip         <- el zip que se instala primero
  repo/addons.xml, repo/addons.xml.md5
  repo/<addon_id>/<addon_id>-<version>.zip (+ icon/fanart)
"""
import argparse
import hashlib
import os
import re
import shutil
import zipfile
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
REPO_VERSION = '1.0.0'
EXCLUDE = re.compile(r'(__pycache__|\.pyc$|\.pyo$|\.git|\.tpl$|\.DS_Store)')


def render_repository_addon(base_url):
    folder = os.path.join(SRC, 'repository.andinoidtv')
    with open(os.path.join(folder, 'addon.xml.tpl'), encoding='utf-8') as fh:
        text = fh.read().format(version=REPO_VERSION, base_url=base_url)
    with open(os.path.join(folder, 'addon.xml'), 'w', encoding='utf-8') as fh:
        fh.write(text)


def addon_info(folder):
    tree = ET.parse(os.path.join(folder, 'addon.xml'))
    root = tree.getroot()
    return root.get('id'), root.get('version')


def zip_addon(folder, dest_dir):
    addon_id, version = addon_info(folder)
    os.makedirs(dest_dir, exist_ok=True)
    zip_path = os.path.join(dest_dir, f'{addon_id}-{version}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for base, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not EXCLUDE.search(d)]
            for name in sorted(files):
                if EXCLUDE.search(name):
                    continue
                full = os.path.join(base, name)
                rel = os.path.relpath(full, os.path.dirname(folder))
                zf.write(full, rel)
    for asset in ('icon.png', 'fanart.jpg'):
        src = os.path.join(folder, asset)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(dest_dir, asset))
    return addon_id, version, zip_path


def addons_xml(folders, out_repo):
    parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<addons>']
    for folder in folders:
        with open(os.path.join(folder, 'addon.xml'), encoding='utf-8') as fh:
            text = fh.read()
        text = re.sub(r'<\?xml[^>]*\?>', '', text).strip()
        parts.append(text)
    parts.append('</addons>')
    data = '\n'.join(parts) + '\n'
    with open(os.path.join(out_repo, 'addons.xml'), 'w', encoding='utf-8') as fh:
        fh.write(data)
    md5 = hashlib.md5(data.encode('utf-8')).hexdigest()
    with open(os.path.join(out_repo, 'addons.xml.md5'), 'w', encoding='utf-8') as fh:
        fh.write(md5)


def link_list(title, entries):
    rows = '\n'.join(f'<a href="{href}">{href}</a><br>' for href in entries)
    return (f'<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>{title}</title></head>\n'
            f'<body>\n<h1>{title}</h1>\n{rows}\n</body></html>\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', required=True)
    parser.add_argument('--repo', default='andinoidtv')
    parser.add_argument('--out', default=os.path.join(ROOT, 'docs'))
    parser.add_argument('--base-url', default=None, help='Sobrescribe la URL base (pruebas locales)')
    args = parser.parse_args()

    base_url = args.base_url or f'https://{args.user}.github.io/{args.repo}'
    render_repository_addon(base_url)

    out = args.out
    if os.path.exists(out):
        shutil.rmtree(out)
    out_repo = os.path.join(out, 'repo')
    os.makedirs(out_repo)

    folders = [os.path.join(SRC, d) for d in sorted(os.listdir(SRC))
               if os.path.exists(os.path.join(SRC, d, 'addon.xml'))]
    built = []
    for folder in folders:
        addon_id, version, zip_path = zip_addon(folder, os.path.join(out_repo, os.path.basename(folder)))
        built.append((addon_id, version, zip_path))
        with open(os.path.join(out_repo, addon_id, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(link_list(addon_id, [os.path.basename(zip_path)]))
    addons_xml(folders, out_repo)

    repo_zip = next(p for a, v, p in built if a == 'repository.andinoidtv')
    root_zip = os.path.join(out, os.path.basename(repo_zip))
    shutil.copy(repo_zip, root_zip)
    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(link_list('Andinoid TV', [os.path.basename(root_zip)]))
    with open(os.path.join(out, '.nojekyll'), 'w') as fh:
        fh.write('')
    with open(os.path.join(out_repo, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(link_list('Andinoid TV repo', ['addons.xml'] + [f'{a}/' for a, v, p in built]))

    print('Base URL:', base_url)
    for addon_id, version, zip_path in built:
        print(f'  {addon_id} {version} -> {os.path.relpath(zip_path, out)}')


if __name__ == '__main__':
    main()
