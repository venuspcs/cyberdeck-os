# Seed Ocean only when the user has not chosen a theme yet.
# A later change in System Settings must survive the next login.
if [ -n "${HOME:-}" ] && [ -x /usr/bin/kwriteconfig6 ] && [ -x /usr/bin/kreadconfig6 ]; then
	theme="$(kreadconfig6 --file kdeglobals --group Sounds --key Theme 2>/dev/null || true)"
	if [ -z "$theme" ]; then
		kwriteconfig6 --file kdeglobals --group Sounds --key Theme ocean
	fi
	enabled="$(kreadconfig6 --file kdeglobals --group Sounds --key Enable 2>/dev/null || true)"
	if [ -z "$enabled" ]; then
		kwriteconfig6 --file kdeglobals --group Sounds --key Enable true
	fi
fi
