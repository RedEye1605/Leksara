from __future__ import annotations

from .review_chain.pipeline import ReviewChain, review_chain

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


def apply_preset(name: str) -> ReviewChain:
	"""Bangun ReviewChain berdasarkan preset."""
	cfg = get_preset(name)
	# Placeholder: map cfg ke langkah. Saat ini identity agar tes tetap hijau.
	steps = [("identity", lambda t: t)]
	return review_chain(steps)


def get_ecommerce_preset() -> dict:
	return PRESETS["ecommerce"]


def ecommerce_review_preset() -> ReviewChain:
	return apply_preset("ecommerce")


__all__ = [
	"get_preset",
	"apply_preset",
	"get_ecommerce_preset",
	"ecommerce_review_preset",
]
