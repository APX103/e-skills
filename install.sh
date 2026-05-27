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

cleanup_legacy_skill_symlinks() {
    local target_dir="$1"
    local legacy_name

    for legacy_name in build think research; do
        local legacy="$target_dir/$legacy_name"

        [ -L "$legacy" ] || continue

        local link_target
        link_target="$(readlink "$legacy")"
        case "$link_target" in
            "$SKILLS_DIR"/skills/"$legacy_name"|"$SKILLS_DIR"/skills/"$legacy_name"/)
                rm "$legacy"
                echo "  $legacy_name: removed stale symlink from $(basename "$(dirname "$target_dir")")"
                ;;
        esac
    done
}

for target_dir in "${TARGET_DIRS[@]}"; do
    mkdir -p "$target_dir"
    echo ""
    echo "Target: $target_dir"
    cleanup_legacy_skill_symlinks "$target_dir"

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
            for target in "$target_dir"/*; do
                [ -L "$target" ] || continue
                link_target="$(readlink "$target")"
                case "$link_target" in
                    "$SKILLS_DIR"/skills/*|"$SKILLS_DIR"/skills/*/)
                        echo "    $(basename "$target") -> $link_target"
                        ;;
                esac
            done
        done
        echo ""
        echo "Skills are symlinked into Claude Code, Codex, Hermes, and generic agent skill directories."
        echo "git pull in this repo will auto-update them."
        ;;
    uninstall)
        echo "Done."
        ;;
esac
