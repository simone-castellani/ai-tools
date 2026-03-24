#!/usr/bin/env bash
# install.sh – Install ai-tools agents and skills via symbolic links.

set -euo pipefail

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

info()    { printf '\033[0;34m[info]\033[0m  %s\n' "$*"; }
success() { printf '\033[0;32m[ok]\033[0m    %s\n' "$*"; }
warn()    { printf '\033[0;33m[warn]\033[0m  %s\n' "$*"; }
error()   { printf '\033[0;31m[error]\033[0m %s\n' "$*" >&2; }

usage() {
  cat <<'EOF'
install.sh – Install ai-tools agents and skills via symbolic links.

Usage:
  ./install.sh [OPTIONS]

Options:
  --tool <name>   Target tool to install for: claude, opencode, or all (default: all)
  --scope <name>  Installation scope: user or project (default: user)
  --dry-run       Print what would be done without making any changes
  -h, --help      Show this help message
EOF
  exit 0
}

# Create a symbolic link, backing up any existing file.
make_link() {
  local src="$1"
  local dest="$2"

  if [ "$DRY_RUN" = true ]; then
    info "(dry-run) ln -s $src -> $dest"
    return
  fi

  mkdir -p "$(dirname "$dest")"

  if [ -L "$dest" ]; then
    local existing_target
    existing_target="$(readlink "$dest")"
    if [ "$existing_target" = "$src" ]; then
      info "Already linked: $dest"
      return
    fi
    warn "Replacing existing symlink: $dest -> $existing_target"
    rm "$dest"
  elif [ -e "$dest" ]; then
    warn "Backing up existing file: $dest -> ${dest}.bak"
    mv "$dest" "${dest}.bak"
  fi

  ln -s "$src" "$dest"
  success "Linked: $dest -> $src"
}

# ---------------------------------------------------------------------------
# Installers
# ---------------------------------------------------------------------------

install_claude() {
  local scope="$1"
  local agents_dir

  if [ "$scope" = "project" ]; then
    agents_dir="$(pwd)/.claude/agents"
  else
    agents_dir="${HOME}/.claude/agents"
  fi

  info "Installing Claude Code agents to: $agents_dir"

  for agent_file in "$REPO_DIR/agents"/*.md; do
    [ -f "$agent_file" ] || continue
    local dest="$agents_dir/$(basename "$agent_file")"
    make_link "$agent_file" "$dest"
  done
}

install_opencode() {
  local scope="$1"
  local base_dir

  if [ "$scope" = "project" ]; then
    base_dir="$(pwd)/.opencode"
  else
    base_dir="${HOME}/.config/opencode"
  fi

  local agents_dir="$base_dir/agents"
  local skills_dir="$base_dir/skills"

  info "Installing OpenCode agents to: $agents_dir"

  for agent_file in "$REPO_DIR/agents"/*.md; do
    [ -f "$agent_file" ] || continue
    local name
    name="$(basename "$agent_file" .md)"
    local dest="$agents_dir/${name}.md"
    make_link "$agent_file" "$dest"
  done

  info "Installing OpenCode skills to: $skills_dir"

  for skill_dir in "$REPO_DIR/skills"/*/; do
    [ -d "$skill_dir" ] || continue
    local name
    name="$(basename "$skill_dir")"
    local dest="$skills_dir/$name"
    make_link "$skill_dir" "$dest"
  done
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

TOOL="all"
SCOPE="user"
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      TOOL="${2:-}"
      if [[ -z "$TOOL" ]]; then
        error "--tool requires a value: claude, opencode, or all"
        exit 1
      fi
      shift 2
      ;;
    --scope)
      SCOPE="${2:-}"
      if [[ -z "$SCOPE" ]]; then
        error "--scope requires a value: user or project"
        exit 1
      fi
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      error "Unknown option: $1"
      usage
      ;;
  esac
done

# Validate arguments
case "$TOOL" in
  claude|opencode|all) ;;
  *)
    error "Invalid --tool value '$TOOL'. Valid values: claude, opencode, all"
    exit 1
    ;;
esac

case "$SCOPE" in
  user|project) ;;
  *)
    error "Invalid --scope value '$SCOPE'. Valid values: user, project"
    exit 1
    ;;
esac

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if [ "$DRY_RUN" = true ]; then
  warn "Dry-run mode enabled – no changes will be made."
fi

info "Repository: $REPO_DIR"
info "Tool:       $TOOL"
info "Scope:      $SCOPE"
echo

case "$TOOL" in
  claude)
    install_claude "$SCOPE"
    ;;
  opencode)
    install_opencode "$SCOPE"
    ;;
  all)
    install_claude "$SCOPE"
    install_opencode "$SCOPE"
    ;;
esac

echo
success "Done."
