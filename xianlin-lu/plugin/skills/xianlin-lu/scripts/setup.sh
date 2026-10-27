#!/bin/sh
# Find a library either in a standalone checkout or in this repository's xianlin-lu/ directory.
# When installed outside a checkout, clone the owning repository into ~/.xianlin-lu and use its xianlin-lu/ subtree.
set -e
REPO=${XIANLIN_LU_REPO:-https://github.com/XianlinLu/Cinema-Craft.git}
if [ -n "$XIANLIN_LU_HOME" ]; then
  REPO_ROOT=$XIANLIN_LU_HOME
elif top=$(git rev-parse --show-toplevel 2>/dev/null); then
  if [ -f "$top/AGENTS.md" ] && [ -d "$top/core/render" ]; then REPO_ROOT=$top
  elif [ -f "$top/xianlin-lu/AGENTS.md" ] && [ -d "$top/xianlin-lu/core/render" ]; then REPO_ROOT=$top
  else REPO_ROOT=$HOME/.xianlin-lu
  fi
else
  REPO_ROOT=$HOME/.xianlin-lu
fi
case "$REPO_ROOT" in /*) ;; *) REPO_ROOT=$(pwd)/$REPO_ROOT ;; esac
if [ -f "$REPO_ROOT/AGENTS.md" ] && [ -d "$REPO_ROOT/core/render" ]; then LIB=$REPO_ROOT; else LIB=$REPO_ROOT/xianlin-lu; fi
is_lib() { [ -f "$1/AGENTS.md" ] && [ -d "$1/core/render" ]; }

apply_sparse() {
  if [ "$LIB" = "$REPO_ROOT" ]; then prefix=''; else prefix='/xianlin-lu'; fi
  set -- "$prefix/*" "!$prefix/styles/*/demo/" "!$prefix/styleboard/" "!$prefix/docs/frames/" "!$prefix/docs/cover.jpg" "!$prefix/docs/opuscar98.jpg" "!$prefix/styles/*/poster.jpg" \
    $(git -C "$REPO_ROOT" sparse-checkout list 2>/dev/null | grep -E "^$prefix/styles/[^/*]+/(demo/|poster\.jpg)$" || true)
  git -C "$REPO_ROOT" sparse-checkout set --no-cone "$@" 2>/dev/null || git -C "$REPO_ROOT" sparse-checkout disable || true
}

if [ "$(git -C "$REPO_ROOT" config --get xianlin-lu.managed 2>/dev/null)" = true ]; then
  [ "$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null)" = "$REPO" ] || git -C "$REPO_ROOT" remote set-url origin "$REPO"
  if err=$(git -C "$REPO_ROOT" fetch --quiet --depth 1 origin main 2>&1 && git -C "$REPO_ROOT" reset --quiet --hard FETCH_HEAD 2>&1); then apply_sparse
  else echo "! could not update $REPO_ROOT (offline?); using the local copy. git: $err" | head -3; fi
elif ! is_lib "$LIB"; then
  [ -e "$REPO_ROOT" ] && [ -n "$(ls -A "$REPO_ROOT" 2>/dev/null)" ] && { echo "✗ $REPO_ROOT exists but is not the xianlin-lu repository. Set XIANLIN_LU_HOME to another folder."; exit 1; }
  command -v git >/dev/null || { echo "✗ git is needed to download the library"; exit 1; }
  echo "↓ downloading the style library into $REPO_ROOT"
  git clone --quiet --depth 1 --filter=blob:none --sparse --branch main "$REPO" "$REPO_ROOT" || { rm -rf "$REPO_ROOT"; echo "✗ download failed (offline?)"; exit 1; }
  if [ "$LIB" != "$REPO_ROOT" ]; then apply_sparse; fi
  git -C "$REPO_ROOT" config xianlin-lu.managed true
fi
LIB=$(cd "$LIB" && pwd -P)
sig() { cat "$@" 2>/dev/null | cksum | cut -d' ' -f1; }
pysig() { echo "$(sig "$1")-$("$LIB/.venv/bin/python" -V 2>&1 | cut -d. -f1,2)"; }
req() { [ "$1" = core ] && echo "$LIB/requirements.txt" || echo "$LIB/requirements-$1.txt"; }
node_ok() { [ "$(cat "$LIB/node_modules/.xianlin-lu-ok" 2>/dev/null)" = "$(sig "$LIB/package.json" "$LIB/package-lock.json")" ]; }
py_ok() { [ "$(cat "$LIB/.venv/.xianlin-lu-$1" 2>/dev/null)" = "$(pysig "$(req "$1")")" ]; }
find_py() { for c in python3.12 python3.13 python3.11 python3; do "$c" -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null && { echo "$c"; return 0; }; done; return 1; }
case "$1" in
  deps)
    shift; tiers=core
    for t in "$@"; do case $t in voice|music) tiers="$tiers $t" ;; *) echo "usage: sh setup.sh deps [voice] [music]"; exit 1 ;; esac; done
    cd "$LIB"
    command -v npm >/dev/null || { echo "✗ npm not found: install Node 20+ first"; exit 1; }
    if ! node_ok; then npm install --no-audit --no-fund --loglevel=error; [ "$(git -C "$REPO_ROOT" config --get xianlin-lu.managed 2>/dev/null)" = true ] && git -C "$REPO_ROOT" checkout -q -- xianlin-lu/package.json xianlin-lu/package-lock.json package.json package-lock.json 2>/dev/null || true; sig package.json package-lock.json > node_modules/.xianlin-lu-ok; fi
    node node_modules/playwright-core/cli.js install chromium-headless-shell
    [ ! -e .venv ] || .venv/bin/python -c pass 2>/dev/null || { echo "! $LIB/.venv is broken; making it again"; rm -rf .venv; }
    if [ ! -x .venv/bin/python ]; then if command -v uv >/dev/null; then uv venv --quiet --python 3.12 .venv; else py=$(find_py) || { echo "✗ Python 3.11+ is needed (or install uv, which fetches it)"; exit 1; }; "$py" -m venv .venv; fi; fi
    for t in $tiers; do py_ok "$t" && continue; if command -v uv >/dev/null; then uv pip install --quiet --python .venv/bin/python -r "$(req "$t")"; else .venv/bin/python -m pip install --quiet --disable-pip-version-check -r "$(req "$t")"; fi; pysig "$(req "$t")" > ".venv/.xianlin-lu-$t"; done
    case " $tiers " in *" voice "*) [ -f core/tts/kokoro-v1.0.onnx ] && [ -f core/tts/voices-v1.0.bin ] || sh tools/fetch.sh voice ;; esac
    ;;
  demo)
    [ -n "$2" ] && [ -f "$LIB/styles/$2/STYLE.md" ] || { echo "usage: sh setup.sh demo <slug> (slugs: $LIB/styles/README.md)"; exit 1; }
    if git -C "$REPO_ROOT" sparse-checkout list >/dev/null 2>&1 && ! git -C "$REPO_ROOT" sparse-checkout list | grep -qx "$([ "$LIB" = "$REPO_ROOT" ] && echo "/styles/$2/demo/" || echo "/xianlin-lu/styles/$2/demo/")"; then
      if [ "$LIB" = "$REPO_ROOT" ]; then git -C "$REPO_ROOT" sparse-checkout add "/styles/$2/demo/" "/styles/$2/poster.jpg"
      else git -C "$REPO_ROOT" sparse-checkout add "/xianlin-lu/styles/$2/demo/" "/xianlin-lu/styles/$2/poster.jpg"; fi
    fi
    echo "demo source: $LIB/styles/$2/demo"
    echo "demo poster: $LIB/styles/$2/poster.jpg"
    ;;
esac
miss=""
if command -v node >/dev/null; then [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 20 ] || miss="$miss node20+(found $(node -v))"; else miss="$miss node20+"; fi
command -v ffmpeg >/dev/null || miss="$miss ffmpeg"
command -v uv >/dev/null || find_py >/dev/null || miss="$miss python3.11+(or uv)"
[ -n "$miss" ] && echo "! missing:$miss"
node_ok && py_ok core || echo "! packages not installed yet: run 'sh setup.sh deps' before the first render"
echo "LIB=$LIB"
