#!/bin/bash
set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.claude/skills"
ACTION="${1:-install}"

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

for skill_dir in "$SKILLS_DIR"/skills/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    target="$TARGET_DIR/$skill_name"

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

case "$ACTION" in
    install|update)
        echo ""
        echo "Done. Installed skills:"
        ls -la "$TARGET_DIR" 2>/dev/null | grep "skills/" | awk '{print "  " $NF " -> " $(NF-1) " " $(NF-2)}' || true
        echo ""
        echo "Skills are symlinked. git pull in this repo will auto-update them."
        ;;
    uninstall)
        echo "Done."
        ;;
esac
