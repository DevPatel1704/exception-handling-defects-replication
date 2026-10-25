#!/usr/bin/env bash
# Run a command inside the `ehrepl` conda env without `conda activate` / `conda run`
# (concurrent `conda run` calls on Windows race on a shared temp file).
# Usage: ./envrun.sh Rscript src/reproduce/run_original.R fixed
#        ./envrun.sh python src/ml/train_eval.py
set -euo pipefail
if [ -z "${EHREPL_PREFIX:-}" ]; then
  EHREPL_PREFIX="$(conda env list | awk '$1=="ehrepl"{print $NF}')"
fi
P="$EHREPL_PREFIX"
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    P="$(cygpath -u "$P")"
    export PATH="$P:$P/Library/mingw-w64/bin:$P/Library/usr/bin:$P/Library/bin:$P/Scripts:$P/bin:$P/Lib/R/bin/x64:$PATH"
    export JAVA_HOME="$(cygpath -w "$P/Library")" ;;
  *)
    export PATH="$P/bin:$PATH"; export JAVA_HOME="$P" ;;
esac
export CONDA_PREFIX="$EHREPL_PREFIX"
export R_HOME="${R_HOME:-}"; unset R_HOME
exec "$@"
