PRESETS = {
	"default": {
		"remove_empty": True,
		"to_lowercase": True,
		"strip_whitespace": True
	},
	"strict": {
		"remove_empty": True,
		"to_lowercase": True,
		"strip_whitespace": True,
		"remove_special_chars": True
	}
}

def get_preset(name):
	"""Mengambil preset konfigurasi berdasarkan nama."""
	return PRESETS.get(name, PRESETS["default"])
