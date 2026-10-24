#!/usr/bin/env bash
# Download the authors' replication package (MSR'18, de Padua & Shang) into external/.
# Idempotent. Verifies SHA-256 of every downloaded archive against the values recorded on 2026-10-24.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
EXT="$ROOT/external"
mkdir -p "$EXT/downloads/bin"
cd "$EXT/downloads"

BASE=https://guipadua.github.io/resources
for f in eh-model-defects2018_data_without_missing.zip \
         eh-model-defects2018_scripts_with_input_data.zip \
         eh-model-defects2018-0-DataSourcesAnalysis.html \
         eh-model-defects2018-1-Model_Construction.html \
         eh-model-defects2018_cr.pdf; do
  [ -f "$f" ] || curl -sSL -o "$f" "$BASE/$f"
done
( cd bin
  [ -f JTratch-Rel.zip ] || curl -sSLO https://github.com/guipadua/JTratch/releases/download/2017icpc_era_cr/JTratch-Rel.zip
  [ -f NTratch-Rel.zip ] || curl -sSLO https://github.com/guipadua/NTratch/releases/download/2017icpc_era_cr/NTratch-Rel.zip )

sha256sum -c <<'EOF'
44d32a58cb7a4f1b3f30422c4c1c57e7fc8f0aa1a0f014b413a1683772d94123  eh-model-defects2018-0-DataSourcesAnalysis.html
7cf367be8af49c1702a76afa1063e69084d8414eccdd5bb0c45cba51e6b47cd5  eh-model-defects2018-1-Model_Construction.html
17cea4b2b6d89479517b9cb461e39b043f4d15157e482ab2c0c80b3b20dafe0d  eh-model-defects2018_cr.pdf
6a8eee1f5e5940c80e1004aba2187dfdd6b353c8d6f5761ed6f69044bdfc2610  eh-model-defects2018_data_without_missing.zip
2d6387a9ee0bdbd2a8081e4bf53f9400b0bf4ba6c6b6b87e4d0e46cc73747eaa  eh-model-defects2018_scripts_with_input_data.zip
bfff85284777f7f6c5e8ce1ead088bc7f8caf2a3439fc58683c72037626a1a51  bin/JTratch-Rel.zip
64fd0d4a77c46dd71d3d8bdbca1f855fee834f27795e37e8dd08cd5acf267840  bin/NTratch-Rel.zip
EOF

cd "$EXT"
[ -d data_without_missing ]    || unzip -q downloads/eh-model-defects2018_data_without_missing.zip -d data_without_missing
[ -d scripts_with_input_data ] || unzip -q downloads/eh-model-defects2018_scripts_with_input_data.zip -d scripts_with_input_data
rm -rf data_without_missing/__MACOSX scripts_with_input_data/__MACOSX

# Exception-flow analyzers at the tag the authors created for this paper.
[ -d JTratch ] || { git clone -q https://github.com/guipadua/JTratch.git JTratch && git -C JTratch checkout -q eh-model-defects2018; }
[ -d NTratch ] || { git clone -q https://github.com/guipadua/NTratch.git NTratch && git -C NTratch checkout -q eh-model-defects2018; }
echo "JTratch @ $(git -C JTratch rev-parse HEAD)"
echo "NTratch @ $(git -C NTratch rev-parse HEAD)"

# Provenance copy of the released merged dataset (small, committed).
mkdir -p "$ROOT/data/original"
cp data_without_missing/all_no_missing.csv "$ROOT/data/original/all_no_missing.csv"
echo "OK"
