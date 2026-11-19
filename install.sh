#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
SKILLS=("panduan-kti-unila" "riset-dan-sidang-ilmiah")

TARGET_ROOTS=(
  "$HOME/.gemini/config/skills"
  "$HOME/.gemini/antigravity/skills"
  "$HOME/.gemini/skills"
  "$HOME/.agents/skills"
  "$HOME/.claude/skills"
)

for root in "${TARGET_ROOTS[@]}"; do
  mkdir -p "$root"
  for name in "${SKILLS[@]}"; do
    rm -rf "$root/$name"
    cp -R "$SKILLS_SRC/$name" "$root/$name"
    echo "[OK] Terpasang: $root/$name"
  done
done

echo ""
echo "Seluruh skill berhasil dipasang! Silakan mulai ulang sesi chat AI Agent Anda."
