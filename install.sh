#!/bin/bash
set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "$0")" && pwd)"
ACTION="${1:-install}"
TARGET_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
    "$HOME/.hermes/skills"
    "$HOME/.agents/skills"
)

case "$ACTION" in
    install)
        echo "Installing skills from $SKILLS_DIR ..."
        ;;
    update)
        echo "Updating skills ..."
        ;;
    uninstall)
        echo "Uninstalling skills ..."
        ;;
    *)
        echo "Usage: $0 [install|update|uninstall]"
        exit 1
        ;;
esac

cleanup_legacy_research_symlink() {
    local target_dir="$1"
    local legacy="$target_dir/research"

    [ -L "$legacy" ] || return 0

    local link_target
    link_target="$(readlink "$legacy")"
    case "$link_target" in
        "$SKILLS_DIR"/skills/research|"$SKILLS_DIR"/skills/research/)
            rm "$legacy"
            echo "  research: removed stale symlink from $(basename "$(dirname "$target_dir")")"
            ;;
    esac
}

for target_dir in "${TARGET_DIRS[@]}"; do
    mkdir -p "$target_dir"
    echo ""
    echo "Target: $target_dir"
    cleanup_legacy_research_symlink "$target_dir"

    for skill_dir in "$SKILLS_DIR"/skills/*/; do
        [ -d "$skill_dir" ] || continue
        skill_name="$(basename "$skill_dir")"
        target="$target_dir/$skill_name"

        case "$ACTION" in
            install|update)
                if [ -L "$target" ]; then
                    rm "$target"
                    ln -s "$skill_dir" "$target"
                    echo "  $skill_name: symlink updated"
                elif [ -d "$target" ]; then
                    echo "  $skill_name: exists as directory (not symlink), skipping. Delete $target manually first."
                else
                    ln -s "$skill_dir" "$target"
                    echo "  $skill_name: symlink created"
                fi
                ;;
            uninstall)
                if [ -L "$target" ]; then
                    rm "$target"
                    echo "  $skill_name: removed symlink"
                elif [ -d "$target" ]; then
                    echo "  $skill_name: not a symlink, skipping. Delete manually if needed."
                else
                    echo "  $skill_name: not installed"
                fi
                ;;
        esac
    done
done

case "$ACTION" in
    install|update)
        echo ""
        echo "Done. Installed skills:"
        for target_dir in "${TARGET_DIRS[@]}"; do
            echo "  $target_dir"
            ls -la "$target_dir" 2>/dev/null | grep "engineer_skills/skills/" | awk '{print "    " $NF " -> " $(NF-1) " " $(NF-2)}' || true
        done
        echo ""
        echo "Skills are symlinked into Claude Code, Codex, Hermes, and generic agent skill directories."
        echo "git pull in this repo will auto-update them."
        ;;
    uninstall)
        echo "Done."
        ;;
esac
