#!/usr/bin/env bash
# setup.sh — Wire agent-toolkit into Claude and GitHub Copilot customizations
# Safe to re-run. Never overwrites existing non-symlink files.

set -euo pipefail
shopt -s nullglob

REPO="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

link() {
  local src="$1" dst="$2" label="$3"
  if [ -L "$dst" ]; then
    echo "  [skip]    $label (symlink already exists)"
  elif [ -e "$dst" ]; then
    echo -e "  ${YELLOW}[conflict]${NC} $label (file exists and is not a symlink — leaving untouched)"
    echo "             Existing: $dst"
    echo "             Repo src: $src"
  else
    ln -s "$src" "$dst"
    echo -e "  ${GREEN}[linked]${NC}  $label"
  fi
}

echo "agent-toolkit setup"
echo "Repo: $REPO"
echo ""

# ── Agents ──────────────────────────────────────────────────────────────────
echo "Agents → $CLAUDE_DIR/agents/"
mkdir -p "$CLAUDE_DIR/agents"
for f in "$REPO"/agents/*.md; do
  name="$(basename "$f")"
  link "$f" "$CLAUDE_DIR/agents/$name" "agents/$name"
done
echo ""

# ── Commands (prompts → slash commands) ─────────────────────────────────────
echo "Commands → $CLAUDE_DIR/commands/"
mkdir -p "$CLAUDE_DIR/commands"
for f in "$REPO"/prompts/*.md; do
  name="$(basename "$f")"
  link "$f" "$CLAUDE_DIR/commands/$name" "commands/$name"
done
echo ""

# ── Skills ──────────────────────────────────────────────────────────────────
echo "Skills → $CLAUDE_DIR/skills/rmatt"
SKILLS_SRC="$REPO/skills/rmatt/skills"
SKILLS_DST="$CLAUDE_DIR/skills/rmatt"
mkdir -p "$CLAUDE_DIR/skills"
link "$SKILLS_SRC" "$SKILLS_DST" "skills/rmatt → (all skills)"
echo ""

# ── CLAUDE.md (BigPurple instructions) ──────────────────────────────────────
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
MARKER="# BEGIN: agent-toolkit/bigpurple"
echo "CLAUDE.md → $CLAUDE_MD"
if grep -qF "$MARKER" "$CLAUDE_MD" 2>/dev/null; then
  echo "  [skip]    BigPurple instructions already present"
else
  {
    printf '\n'
    echo "$MARKER"
    cat "$REPO/instructions/bigpurple.instructions.md"
    echo "# END: agent-toolkit/bigpurple"
  } >> "$CLAUDE_MD"
  echo -e "  ${GREEN}[added]${NC}   BigPurple instructions appended"
fi
echo ""

# ── GitHub Copilot (User Profile + Personal Skills) ─────────────────────────
COPILOT_PROFILE_DIR="${VSCODE_USER_PROMPTS_FOLDER:-$HOME/Library/Application Support/Code/User/prompts}"
COPILOT_SKILLS_DIR="$HOME/.copilot/skills"

echo "GitHub Copilot profile files → $COPILOT_PROFILE_DIR/"
mkdir -p "$COPILOT_PROFILE_DIR"

# Instructions (*.instructions.md) → profile prompts folder
for f in "$REPO"/instructions/*.instructions.md; do
  name="$(basename "$f")"
  link "$f" "$COPILOT_PROFILE_DIR/$name" "$name"
done

# Prompts (*.prompt.md) → profile prompts folder
for f in "$REPO"/prompts/*.prompt.md; do
  name="$(basename "$f")"
  link "$f" "$COPILOT_PROFILE_DIR/$name" "$name"
done

# Agents (*.agent.md) → profile prompts folder
for f in "$REPO"/agents/*.agent.md; do
  name="$(basename "$f")"
  link "$f" "$COPILOT_PROFILE_DIR/$name" "$name"
done

echo "GitHub Copilot personal skills → $COPILOT_SKILLS_DIR/"
mkdir -p "$COPILOT_SKILLS_DIR"

# Skills (*/skills/<skill-name>/SKILL.md) → ~/.copilot/skills/<skill-name>/
for f in "$REPO"/skills/*/skills/*; do
  [ -d "$f" ] || continue
  name="$(basename "$f")"
  link "$f" "$COPILOT_SKILLS_DIR/$name" ".copilot/skills/$name"
done
echo ""

echo "Done. To update: git pull in $REPO"
echo "Conflicts above must be resolved manually (delete the existing file, then re-run)."
