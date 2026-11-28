# Write the Ocean sound theme into the user kdeglobals before Plasma starts.
# Debian's look-and-feel apply creates that file without a [Sounds] group.
# Canberra then falls back to the freedesktop theme: old sounds for some
# events, and silence for login, logout, and the ids that theme lacks.
if [ -n "${HOME:-}" ] && [ -x /usr/bin/kwriteconfig6 ]; then
	kwriteconfig6 --file kdeglobals --group Sounds --key Theme ocean
	kwriteconfig6 --file kdeglobals --group Sounds --key Enable true
fi
