# Examples and Recipes

Each scenario below corresponds to a core feature described in `docs/features.md`. Copy the snippets into a notebook or script and adapt them to your data sources.

---

## 1. Audit a raw review feed with CartBoard

```python
import pandas as pd
from leksara.frames.cartboard import get_flags, get_stats, noise_detect

reviews = pd.DataFrame(
    {
        "review_id": [21, 22, 23],
        "channel": ["Tokopedia", "Shopee", "Lazada"],
        "text": [
            "Produk kece bgt!!! Email saya user@mail.id ⭐⭐⭐⭐⭐",
            "Pengiriman lambat :( Hubungi 0812-3456-7890",
            "Oke lah, cuma packing agak rusak",
        ],
    }
)

flags = get_flags(reviews, text_column="text")
stats = get_stats(reviews, text_column="text")
noise = noise_detect(reviews, text_column="text", include_normalized=False)

report = flags.join(stats[["review_id", "stats"]].set_index("review_id"), on="review_id")
report = report.join(noise[["review_id", "detect_noise"]].set_index("review_id"), on="review_id")

print(report[["review_id", "pii_flag", "rating_flag", "non_alphabetical_flag"]])
print(report.loc[21, "detect_noise"]["emails"])
```

### What this shows

- `pii_flag` highlights entries that will require masking before sharing with analysts.
- The `stats` dictionary exposes per-review length, word counts, and emoji counts—use it to build dashboards.
- `detect_noise` inventories the raw artefacts (URLs, phones) you can later compare with cleaned text to confirm redaction success.

---

## 2. Clean a Pandas Series using the ecommerce preset

```python
import pandas as pd
from leksara import leksara

df = pd.DataFrame(
    {
        "order_id": [111, 112],
        "review": [
            "<p>MANTUL banget! ⭐⭐⭐⭐⭐ Hubungi CS: +62 812-3333-4444</p>",
            "Barangnya bagus, packaging aman. Rating 4/5.",
        ],
    }
)

df["clean_review"] = leksara(df["review"], preset="ecommerce_review")
print(df[["order_id", "clean_review"]])
```

### Why this works

- The preset bundles PII masking, casing, stopword removal, slang normalisation, and rating replacement steps.
- Inputs that are not strings (for example `NaN`) are returned unchanged, so no pre-filtering is required.

---

## 3. Extend a preset with additional masking

```python
from leksara import leksara
from leksara.core.presets import get_preset
from leksara.function import replace_address, remove_digits

pipeline = get_preset("ecommerce_review")
pipeline["patterns"].append((replace_address, {"mode": "replace", "street": True, "city": True}))
pipeline["functions"].append(remove_digits)

messages = [
    "Alamat lengkap: Jl. Durian No. 12 RT 01 RW 03, Jakarta. Rating: 4/5",
    "Pickup di Mall Central Park lt.3 ya",
]

cleaned = leksara(messages, pipeline=pipeline)
for text in cleaned:
    print(text)
```

### Key takeaways

- You can manipulate the preset dictionary to add new pattern/function steps before running the pipeline.
- Passing component toggles to `replace_address` limits masking to specific address fragments.

---

## 4. Build a reusable ReviewChain for streaming jobs

```python
from leksara import ReviewChain
from leksara.function import (
    case_normal,
    replace_phone,
    replace_email,
    remove_stopwords,
    remove_punctuation,
)

chain = ReviewChain.from_steps(
    patterns=[
        (replace_phone, {"mode": "replace"}),
        (replace_email, {"mode": "replace"}),
    ],
    functions=[case_normal, remove_stopwords, remove_punctuation],
)

def clean_event(payload: dict) -> dict:
    processed, metrics = chain.transform([payload["message"]], benchmark=True)
    payload["clean_message"] = processed[0]
    payload["timings"] = metrics
    return payload

# Example event from a queue
event = {"message": "Halo CS, email saya rani@shop.id, nomor 0812333444."}
print(clean_event(event))
```

### Why use `ReviewChain` here?

- You can memoise the chain and reuse it across events instead of rebuilding the pipeline for every message.
- `benchmark=True` exposes per-step timing so you can emit performance metrics to monitoring systems.

---

## 5. Update slang handling at runtime

```python
import json
from pathlib import Path

import leksara.functions.review.advanced as adv
from leksara.function import normalize_slangs

# Load the bundled slang dictionary, extend it, then patch the module-level cache.
slang_path = Path(adv.__file__).resolve().parent.parent / "resources" / "dictionary" / "slangs_dict.json"
with slang_path.open(encoding="utf-8") as fh:
    slang_dict = json.load(fh)

slang_dict.update({"bgst": "bagus", "cmiiw": "tolong koreksi jika salah"})
adv._SLANGS_DICT = slang_dict  # monkeypatch for this process

text = "Produk bgst banget, cmiiw tapi garansinya 2 tahun"
print(normalize_slangs(text))
```

### Important notes

- Many advanced functions keep their dictionaries in module-level caches. Updating the cache before running pipelines lets you experiment without rebuilding the package.
- After monkeypatching, rerun key unit tests (`tests/test_review_advanced.py`) to ensure behaviour remains stable.


