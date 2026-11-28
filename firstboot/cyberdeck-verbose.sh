# Shared terminal behavior for Cyberdeck OS scripts.
# Source this, then call cyberdeck_verbose_begin with a short name.
cyberdeck_verbose_begin() {
	_cd_name="$1"
	shift
	LOG="/var/log/cyberdeck-${_cd_name}.log"
	if [ ! -t 1 ]; then
		if command -v konsole >/dev/null 2>&1; then
			exec konsole --hold -e "$0" "$@"
		fi
	fi
	if [ "$(id -u)" -ne 0 ]; then
		echo "Type your password. Nothing will show as you type."
		exec sudo -- "$0" "$@"
	fi
	mkdir -p /var/log /var/lib/cyberdeck
	touch "$LOG"
	chmod 644 "$LOG" || true
	exec > >(tee -a "$LOG") 2>&1
	echo "======== ${_cd_name} ========"
	echo "Log: $LOG"
}
cyberdeck_step() {
	echo
	echo "-------- $* --------"
}
cyberdeck_apt() {
	cyberdeck_step "apt $*"
	echo "Waiting for the package lock if another installer is using it."
	apt-get -o DPkg::Lock::Timeout=600 "$@"
}
cyberdeck_finish() {
	status="$1"
	shift
	echo
	echo "${status}: $*"
	echo "Log: ${LOG:-/var/log/cyberdeck.log}"
	echo "Press Enter to close."
	read -r _ || true
	if [ "$status" = "ERROR" ]; then
		exit 1
	fi
}
