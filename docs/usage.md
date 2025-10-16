# Penggunaan

```python
import pandas as pd
from leksara.cartboard import build_frame
from leksara.presets import ecommerce_review_preset

texts = ["Barangnya baaaagus banget!!! COD lancar, cs ramah."]
df = build_frame(texts)
chain = ecommerce_review_preset()
df2 = chain.run_on_dataframe(df)
print(df2.head())
```

## Default & Kebijakan


## Orchestrator Cepat

Gunakan utilitas `get_flags`, `get_stats`, dan `noise_detect` untuk mengevaluasi teks mentah sebelum masuk pipeline utama.

```python
from leksara.frames.cartboard import get_flags, get_stats, noise_detect

texts = [
    "Barangnya mantap!!! Email saya user@example.com",
    "<p>Promo 50% di https://shop.id 😀</p> Hubungi 0812 1234 5678",
]

flags = get_flags(texts)
stats = get_stats(texts)
noise = noise_detect(texts)

print(flags[["pii_flag", "non_alphabetical_flag"]])
print(stats[["word_count", "stopwords"]])
print(noise.head())

