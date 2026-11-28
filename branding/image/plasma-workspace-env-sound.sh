# kreadconfig6 merges /etc/xdg, so a system Theme=ocean hides an empty
# user file. Read only the user file. Leave an explicit choice alone.
if [ -n "${HOME:-}" ] && [ -x /usr/bin/kwriteconfig6 ]; then
	cfg="${HOME}/.config/kdeglobals"
	mkdir -p "${HOME}/.config"
	theme="$(awk '
		/^\[Sounds\]/ { in_sounds = 1; next }
		/^\[/ { in_sounds = 0 }
		in_sounds && /^Theme=/ { sub(/^Theme=/, ""); print; exit }
	' "$cfg" 2>/dev/null || true)"
	if [ -z "$theme" ]; then
		kwriteconfig6 --file kdeglobals --group Sounds --key Theme ocean
		kwriteconfig6 --file kdeglobals --group Sounds --key Enable true
	fi
fi
