# Benchmarks

Aktifkan pencatatan waktu (benchmark) pada pipeline untuk melihat lama eksekusi tiap langkah.

```python
from leksara.pipeline import PipelineConfig
from leksara.presets import ecommerce_review_preset

chain = ecommerce_review_preset()
chain.config.benchmark = True
# Setelah run_on_series/dataframe, akses attribute:
# s_out.attrs["benchmark_timings"]
```
