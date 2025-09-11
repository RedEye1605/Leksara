# Presets

Preset `ecommerce_review` menjalankan pembersihan umum, normalisasi slang dan akronim, dan masking PII (phone/email/address/ID).

Gunakan via:

```python
from leksara.presets import ecommerce_review_preset
chain = ecommerce_review_preset()
```
