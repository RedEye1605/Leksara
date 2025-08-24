PRESETS = {
	"default": {
		"remove_stopwords": False,
		"remove_punctuation": True,
		"normalize_case": True,
	},
	"ecommerce": {
		"remove_stopwords": True,
		"remove_punctuation": True,
		"normalize_case": True,
	},
}

def get_preset(name: str):
	"""Mengambil preset konfigurasi berdasarkan nama."""
	return PRESETS.get(name, PRESETS["default"])

def get_ecommerce_preset():
	"""Preset khusus untuk domain e-commerce sesuai kebutuhan test."""
	return PRESETS["ecommerce"]
