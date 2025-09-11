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

- basic_clean: remove_punct=False, remove_digits=False, reduce_repeat=True, max_repeat=2, keep_newline=False, remove_stopwords=False.
- Pipeline preset dapat memilih keep_newline=True untuk pelestarian baris.
- Token masking standar: \<PHONE>, \<EMAIL>, \<ADDRESS>, \<ID>.

