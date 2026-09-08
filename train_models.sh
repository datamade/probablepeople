#!/usr/bin/env bash
#
# Regenerate the CRF models, overwriting the committed ones. The training commands
# live in setup.py's `train_model` command, so this is only a thin wrapper.
#
# Usage: ./train_models.sh [hash-seed]     (default: 1, what the committed models use)

set -euo pipefail

cd "$(dirname "$0")"

export PYTHONHASHSEED="${1:-1}"

echo "Training with PYTHONHASHSEED=$PYTHONHASHSEED"
python setup.py train_model

echo
echo "Model fingerprints (sha256, first 16):"
python -c "
import hashlib
import pathlib

for path in sorted(pathlib.Path('probablepeople').glob('*.crfsuite')):
    print(f'  {hashlib.sha256(path.read_bytes()).hexdigest()[:16]}  {path.name}')
"
