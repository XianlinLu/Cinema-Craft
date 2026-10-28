#!/usr/bin/env python3
"""Bundle the complete style specifications for Lumina's text-file importer.

Run from anywhere: python3 tools/build_lumina_skill.py [--check | --verify-import | --repack-existing] [--zip PATH]
The uploaded skill contains data and instructions only; this maintainer script
stays outside it. Style fragments are byte-verifiable against the library.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / 'xianlin-lu'
SKILL = ROOT / 'skills' / 'lumina-canvas-film'
CAP = 29600  # UTF-16 code units; 400-unit margin below the user-confirmed 30,000 limit
TAIL = '\n<!-- END STYLE PAGE -->\n'
REPO = 'https://github.com/XianlinLu/Cinema-Craft'


def units(text):
    return len(text.encode('utf-16-le')) // 2


def blocks(text):
    """Keep paragraphs and fenced examples together, preserving all characters."""
    block = []
    fence = None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        mark = re.match(r'(`{3,}|~{3,})', stripped)
        if mark:
            if fence is None:
                fence = mark.group(1)
            elif mark.group(1)[0] == fence[0] and len(mark.group(1)) >= len(fence):
                fence = None
        block.append(line)
        if not line.strip() and fence is None:
            yield ''.join(block)
            block = []
    if block:
        yield ''.join(block)


def partition_styles(order, sources, manifest):
    """Pack exact source text without summaries, using current importer capacity."""
    generated = {}
    page_no = 1
    page = '# Complete style specifications 01\n\n'
    active = None
    for slug in order:
        raw = sources[slug]
        entry = {'sha256': hashlib.sha256(raw.encode()).hexdigest(), 'parts': []}
        manifest['styles'][slug] = entry
        for block in blocks(raw):
            marker = f'\n<!-- STYLE: {slug} -->\n\n' if active != slug else ''
            if units(page + marker + block + TAIL) > CAP:
                generated[f'references/style-specs-{page_no:02}.md'] = page + TAIL
                page_no += 1
                page = f'# Complete style specifications {page_no:02}\n\n'
                active = None
                marker = f'\n<!-- STYLE: {slug} -->\n\n'
            assert units(page + marker + block + TAIL) <= CAP, f'Atomic block too large: {slug}'
            page += marker
            file = f'references/style-specs-{page_no:02}.md'
            start = len(page)
            page += block
            if active == slug:
                entry['parts'][-1][2] = len(page)
            else:
                entry['parts'].append([file, start, len(page)])
            active = slug
    generated[f'references/style-specs-{page_no:02}.md'] = page + TAIL
    for slug, entry in manifest['styles'].items():
        restored = ''.join(generated[file][start:end] for file, start, end in entry['parts'])
        assert restored == sources[slug], slug
        assert hashlib.sha256(restored.encode()).hexdigest() == entry['sha256'], slug
    return generated


def generate():
    order = re.findall(r'\[`([^`]+)`\]\([^)]*STYLE\.md\)', (LIB / 'styles/README.md').read_text())
    assert order and len(order) == len(set(order)), 'Invalid or duplicate style entries'
    assert set(order) == {p.parent.name for p in (LIB / 'styles').glob('*/STYLE.md')
                          if not p.parent.name.startswith('_')}, 'Index and source styles differ'
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    metadata = {slug: json.loads((LIB / f'styles/{slug}/style.json').read_text()) for slug in order}
    catalog_hash = hashlib.sha256(json.dumps(metadata, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    old_manifest = SKILL / 'references/style-manifest.json'
    # Keep the pinned library revision stable across unrelated skill-only commits.
    if old_manifest.exists():
        previous = json.loads(old_manifest.read_text())
        same = all(hashlib.sha256((LIB / f'styles/{slug}/STYLE.md').read_bytes()).hexdigest()
                   == previous.get('styles', {}).get(slug, {}).get('sha256') for slug in order)
        if same and len(previous.get('styles', {})) == len(order) and previous.get('catalog_sha256') == catalog_hash:
            revision = previous['library_revision']
    manifest = {'format': 1, 'library_repository': REPO, 'library_revision': revision,
                'style_count': len(order), 'offsets': 'Unicode code points; end-exclusive; fragments concatenate in listed order',
                'catalog_sha256': catalog_hash, 'workflow': 'native-video-v6.0', 'styles': {}}
    sources = {slug: (LIB / f'styles/{slug}/STYLE.md').read_text() for slug in order}
    generated = partition_styles(order, sources, manifest)
    generated['references/style-manifest.json'] = json.dumps(manifest, ensure_ascii=False, separators=(',', ':')) + '\n'
    lines = ['# Style index / 风格索引', '',
             f'All {len(order)} styles are included with their full specifications. Names and categories below are canonical.',
             "For new projects, moodboard-visuals.md's native direction choice offers researched visual grammar OR this library. Honor a named compatible style; for a library choice read all its fragments. Record researched directions separately, never as invented catalog slugs. Reuse valid existing approvals.",
             'For the selected slug, read EVERY listed spec file and extract its `<!-- STYLE: slug -->` segment in file order.',
             'A segment ends at the next STYLE marker or END STYLE PAGE marker. Join its pieces without dropping any section.',
             'Do not load the other styles. `style-manifest.json` records exact fragment offsets and SHA-256 checksums.',
             'Paths inside specifications (`demo/`, `DEMO.md`, etc.) are relative to that style in the library, not this import package.',
             'The current native-video workflow takes precedence over legacy code-engine execution examples; retain visual/voice grammar without claiming that engine code or external assets are bundled.',
             f'Library: {REPO}/tree/{revision}/xianlin-lu',
             'Gallery source: the library\'s `styleboard/` folder. Link a playable gallery only if it is available and verified; label a source-directory link as source.',
             'Style metadata below omits demo story descriptions so treatments can be written independently.', '']
    last_category = None
    for slug in order:
        meta = metadata[slug]
        category = (meta['category_en'], meta['category_cn'])
        if category != last_category:
            if last_category is not None:
                lines.append('')
            lines += [f'## {category[0]} / {category[1]}', '',
                      '| English | 中文 | Slug | Fits / use cases | Full specification files |',
                      '|---|---|---|---|---|']
        parts = manifest['styles'][slug]['parts']
        files = ', '.join(f'[{Path(file).name}]({Path(file).name})' for file, _, _ in parts)
        uses = '; '.join(meta.get('uses', [])).replace('|', '/')
        lines.append(f"| {meta['en']} | {meta['cn']} | {slug} | {uses} | {files} |")
        last_category = category
    generated['references/style-index.md'] = '\n'.join(lines) + '\n'
    for name, text in generated.items():
        assert units(text) <= CAP, (name, units(text))
    return generated


def repack_existing():
    """Repack a hash-verified ready bundle without fetching demo/media assets."""
    manifest = json.loads((SKILL / 'references/style-manifest.json').read_text())
    order = list(manifest['styles'])
    sources = {}
    for slug, entry in manifest['styles'].items():
        sources[slug] = ''.join((SKILL / name).read_text()[start:end]
                                for name, start, end in entry['parts'])
        assert hashlib.sha256(sources[slug].encode()).hexdigest() == entry['sha256'], slug
    index = (SKILL / 'references/style-index.md').read_text()
    manifest['workflow'] = 'native-video-v6.0'
    manifest['styles'] = {}
    generated = partition_styles(order, sources, manifest)
    lines = []
    indexed = set()
    for line in index.splitlines():
        cells = line.split('|')
        if len(cells) == 7 and cells[3].strip() in manifest['styles']:
            slug = cells[3].strip()
            indexed.add(slug)
            refs = [part[0] for part in manifest['styles'][slug]['parts']]
            cells[-2] = ' ' + ', '.join(f'[{Path(name).name}]({Path(name).name})' for name in refs) + ' '
            line = '|'.join(cells)
        lines.append(line)
    assert indexed == set(order), 'Style index lost a canonical entry'
    generated['references/style-index.md'] = '\n'.join(lines) + '\n'
    generated['references/style-manifest.json'] = json.dumps(manifest, ensure_ascii=False, separators=(',', ':')) + '\n'
    return generated


def validate(generated, check):
    for relative, content in generated.items():
        path = SKILL / relative
        if check:
            assert path.exists() and path.read_text() == content, f'Out of date: {relative}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    expected = {SKILL / p for p in generated}
    for stale in (SKILL / 'references').glob('style-specs-*.md'):
        if stale not in expected:
            if check:
                raise AssertionError(f'Stale style shard: {stale}')
            stale.unlink()
    return inspect_import()


def inspect_import():
    """Verify the ready importer without requiring the source toolkit or media."""
    files = sorted(p for p in SKILL.rglob('*') if p.is_file())
    directories = [p for p in SKILL.rglob('*') if p.is_dir()]
    total = len(files) + len(directories) + 1
    assert total <= 49, f'Import has {total} items including directories/root (maximum 49)'
    for path in files:
        assert path.suffix in {'.md', '.txt', '.json', '.yaml', '.yml'}, path
        for part in path.relative_to(SKILL).parts:
            assert len(part) <= 64 and re.fullmatch(r'[A-Za-z0-9_-]+(?:\.[a-z]+)?', part), part
        assert units(path.read_text()) <= CAP, (path, units(path.read_text()))
    manifest = json.loads((SKILL / 'references/style-manifest.json').read_text())
    assert manifest['style_count'] == len(manifest['styles'])
    for slug, entry in manifest['styles'].items():
        restored = ''.join((SKILL / name).read_text()[start:end]
                           for name, start, end in entry['parts'])
        assert hashlib.sha256(restored.encode()).hexdigest() == entry['sha256'], slug
    core = [SKILL / 'SKILL.md', SKILL / 'references/production-workflow.md',
            SKILL / 'references/production-requests.md', SKILL / 'references/style-index.md',
            SKILL / 'references/runtime-control.md', SKILL / 'references/characters-voices.md',
            SKILL / 'references/audio-postproduction.md', SKILL / 'references/speech-inputs.md',
            SKILL / 'references/props-assets.md', SKILL / 'references/story-development.md',
            SKILL / 'references/moodboard-visuals.md']
    for path in core:
        text = path.read_text()
        for ref in re.findall(r'`((?:references/)?[a-z0-9-]+\.(?:md|json|yaml))`', text):
            target = SKILL / ref if ref.startswith('references/') or ref == 'SKILL.md' else path.parent / ref
            # The index explicitly identifies demo paths as source-toolkit examples.
            if ref in {'DEMO.md'}:
                continue
            assert target.exists(), f'Broken importer reference: {path.name}: {ref}'
        for link in re.findall(r'\]\((style-specs-[0-9]+\.md)\)', text):
            assert (path.parent / link).exists(), link
    print(f'{len(files)} files; {total} items including directories/root; '
          f'{manifest["style_count"]} complete styles; maximum '
          f'{max(units(p.read_text()) for p in files)} UTF-16 units/file; hashes and references verified')
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--verify-import', action='store_true',
                      help='Check the existing import folder without regenerating from source')
    mode.add_argument('--repack-existing', action='store_true',
                      help='Losslessly repack existing verified style texts at the current cap')
    parser.add_argument('--zip', type=Path)
    args = parser.parse_args()
    if args.verify_import:
        files = inspect_import()
    elif args.repack_existing:
        files = validate(repack_existing(), False)
    else:
        files = validate(generate(), args.check)
    if args.zip:
        args.zip.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.zip, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, path.relative_to(SKILL).as_posix())
        print(f'Import package: {args.zip}')


if __name__ == '__main__':
    main()

