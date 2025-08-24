PRESETS = {
	"default": {
		"remove_stopwords": False,
		"remove_punctuation": True,
		"lowercase": True,
	},
	"ecommerce": {
		"remove_stopwords": True,
		"remove_punctuation": True,
		"lowercase": True,
	},
}

def get_preset(name: str) -> dict:
	"""Mengambil preset konfigurasi berdasarkan nama."""
	return PRESETS.get(name, PRESETS["default"])

def get_ecommerce_preset() -> dict:
	"""Preset khusus untuk domain e-commerce sesuai kebutuhan test."""
	return PRESETS["ecommerce"]
